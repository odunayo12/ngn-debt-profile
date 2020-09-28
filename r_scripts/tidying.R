library(tidyverse)
library(data.table)






map_df_fread <- function(path, pattern = "*.csv") {
  list.files(path, pattern, full.names = TRUE) %>%
    map_df(~ fread(.))
}

DATA_F <- map_df_fread('scrapper/downloads/')

trim_table <- function(raw_data, deat_quarter) {
  raw_data %>%
    names(raw_data) <- gsub(names(raw_data), "\\r", " ") %>% 
    select(-`Debt Category`) %>%
    rename(
      debt_cat = `Amount Outstanding in USD`,
      outstanding_usd_inM = `Amount Outstanding in NGN`,
      outstanding_ngn_inM = X4
    ) %>%
    filter(!is.na(.),
           !is.na(outstanding_ngn_inM),
           str_detect(debt_cat, "Sub", negate = T)) %>%
    mutate(as_at = deat_quarter)
}

trim_table(X1538, "June 2016") %>% view()
jun_30_16 <- trim_table(X1538, "June 2016") %>%
  mutate(
    ext_rate = 283,
    ext_rate = replace(ext_rate, str_detect(debt_cat, "States[*]"), 197),
    remark = "*Actual Domestic Debt Stock for 36 States & the FCT was as at end-December, 2015
CBN Official Exchange rate of 1 USD to 283 NGN as at June 30, 2016 and 197 NGN as at December, 2015 were used IRO FGN and States
Domestic debt, respectively.",
    as_at = "June 2016"
  ) %>% view()

mar_31_16 <- trim_table(X1539, "March 2016") %>%
  mutate(
    ext_rate = 197,
    ext_rate = replace(ext_rate, str_detect(debt_cat, "States[*]"), 168),
    remark = "*Actual Domestic Debt Stock for 36 States & the FCT was as at end-December, 2014
CBN Official Exchange rate of 1 USD to 197 NGN as at March 31, 2016 and 168 NGN as at December, 2014 were used IRO FGN and States
Domestic debt, respectively."
    # # check_val = if_else(
    # #   outstanding_ngn_inM == ext_rate * outstanding_usd_inM,
    # #   "Same",
    # #   "Error"
    # # ),
    # check_val_fig = ext_rate * outstanding_usd_inM
  )

sept_30_2016 <- trim_table(X1973, "September 2016") %>%
  mutate(
    ext_rate = round(outstanding_ngn_inM / outstanding_usd_inM, 0),
    #ext_rate = replace(ext_rate, str_detect(debt_cat, "States[*]"), 168),
    remark = "*Actual Domestic Debt Stock for 36 States & the FCT was as at end-December, 2015"
  ) %>% view()

dec_31_2016 <- trim_table(X1974, "December 2016") %>%
  mutate(
    ext_rate = round(outstanding_ngn_inM / outstanding_usd_inM, 0),
    remark = "*Actual Domestic Debt Stock for 36 States & the FCT was as at end-September, 2016"
  )

mar_31_17 <- trim_table(X2075, "March 2017") %>%
  mutate(
    ext_rate = if_else(
      str_detect(debt_cat, "States[*]"),
      round(outstanding_ngn_inM / outstanding_usd_inM, 0),
      306.35
    ),
    remark = "
*External debt and FGN domestic debt figures are as at March 2017. The domestic debt figures for 31 States are as at December 2016, except for
Ogun State (December 2015) Akwa-Ibom & Rivers (June 2016) and Jigawa and Katsina (March 2016) \rCBN Official Exchange rate of 1 USD to 306.35NGN as at March 31, 2017 was used IRO FGN"
  ) %>% view()

jun_30_17 <- trim_table(X2170, "June 2017") %>%
  mutate(
    ext_rate = 305.9,
    remark = " (i). External Debt & FGN Domestic Debt figures are as at June 30, 2017;
(ii). The Domestic Debt figures for 33 States and the FCT are as at End-December, 2016, except for Ogun State (Dec. 2015) and Akwa- Ibom and
 Rivers States (June, 2016); and,
 (iii). Exchange Rate for all FGN and States’ Domestic Debts is USD/NGN 305.9 which is the CBN Official Rate."
  ) %>% filter(str_detect(debt_cat, "Grand", negate = T)) %>% view()


sept_30_2017 <- trim_table(X2255, "September 2017") %>% 
  mutate(ext_rate = round(outstanding_ngn_inM / outstanding_usd_inM, 0),
         remark ="*Actual Domestic Debt Stock for 36 States & the FCT was as at end-June, 2017" ) %>%
  view()


