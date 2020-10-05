library(tidyverse)
library(data.table)



try_watch <- X1538
try_watch %>% rename_with( ~ gsub("\\r", " ", .x)) %>%
  glimpse() %>%
  view()

map_df_fread <- function(path, pattern = "*.csv") {
  list.files(path, pattern, full.names = TRUE) %>%
    map_df( ~ fread(.))
}

DATA_F <- map_df_fread('scrapper/downloads/')

trim_table <- function(raw_data, deat_quarter) {
  raw_data %>%
    rename_with( ~ gsub("\\r", " ", .x)) %>%
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

#trim_table(X1538, "June 2016") %>% view()

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
  mutate(
    ext_rate = round(outstanding_ngn_inM / outstanding_usd_inM, 0),
    remark = "*Actual Domestic Debt Stock for 36 States & the FCT was as at end-June, 2017"
  ) %>%
  view()

dec_31_2017 <- trim_table(X2380, "December 2017") %>%
  mutate(
    ext_rate = 306,
    ext_rate = replace(ext_rate, str_detect(debt_cat, "States[*]"), 306.75),
    remark = "*External debt and FGN domestic debt figures are as at December 2017. The domestic debt figures for 32 States & the FCT are as at December 2017,
except for 3 States (Akwa Ibom, Katsina, Lagos) are as at September 30, 2017. Borno State (June 2017). \r CBN Official Exchange rate of 1 USD to 306.75NGN as at September 30, 2017 and 1 USD to 306 NGN as at December 31,2017 were used"
  )

mar_31_18 <- X2470 %>%
  select(`Debt Category`, X2, `Amount Outstanding`) %>%
  rename(
    debt_cat = `Debt Category`,
    outstanding_usd_inM = X2,
    outstanding_ngn_inM = `Amount Outstanding`
  ) %>%
  filter(
    !is.na(outstanding_usd_inM),
    str_detect(outstanding_usd_inM, "^in[ ]", negate = T),
    str_detect(debt_cat, "Total", negate = T)
  ) %>%
  mutate(debt_cat =str_trim(str_replace_all(debt_cat, "[A-Z]\\.|\\.", "")),
         ext_rate = 306,
         ext_rate = replace(ext_rate, str_detect(debt_cat, "\\*$"), 305.65),
         remark = " Note: CBN Official Exchange Rate of US$1 to NGN306 as at December 31, 2017 and US$1 to NGN305.65
 as at March 31, 2018 were used for the conversion of External debt stock to Naira") %>%
  view()

trim_value_2_plus <- function(raw_data, as_at, ext_rate_f, ext_rate_2_f, remark_f ) {
  raw_data %>% 
    select(`Debt Category`, X2, `Amount Outstanding`) %>%
    rename(
      debt_cat = `Debt Category`,
      outstanding_usd_inM = X2,
      outstanding_ngn_inM = `Amount Outstanding`
    ) %>%
    filter(
      !is.na(outstanding_usd_inM),
      str_detect(outstanding_usd_inM, "^in[ ]", negate = T),
      str_detect(debt_cat, "Total", negate = T)
    ) %>%
    mutate(debt_cat =str_trim(str_replace_all(debt_cat, "[A-Z]\\.|\\.", "")),
           as_at = as_at,
           ext_rate = ext_rate_f,
           ext_rate = replace(ext_rate, str_detect(debt_cat, "\\*$"), ext_rate_2_f),
           remark = remark_f)
}

trim_value_2_plus(X2470, "March 2018", 306.2, 306.65, "brew") %>% view()
