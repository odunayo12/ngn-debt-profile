library(readr)
library(tidyverse)
# merged_wip_ <- read_csv(
#   "scrapper/downloads/merged_wip_.csv",
#   col_types = cols(
#     `% of Total` = col_character(),
#     `Amount Outstanding` = col_character(),
#     `Amount Outstanding (N-M)` = col_character(),
#     `Amount Outstanding (US$-M)` = col_character(),
#     `Amount Outstanding-(N-M)` = col_character(),
#     `Amount Outstanding-(US$-M)` = col_character(),
#     `Amount Outstanding.1` = col_character(),
#     `Amount-Outstanding` = col_character(),
#     `Amount-Outstanding-(N-M)` = col_character(),
#     `Unnamed: 0.1` = col_character(),
#     `Unnamed: 1` = col_character(),
#     `Unnamed: 10` = col_character(),
#     `Unnamed: 2` = col_character(),
#     `Unnamed: 4` = col_character(),
#     `Unnamed: 5` = col_character(),
#     `Unnamed: 6` = col_character(),
#     `Unnamed: 8` = col_character()
#   )
# )
# View(merged_wip_)
#
# # clean column names
# names(merged_wip_) <- gsub(" |:", "_", names(merged_wip_))
# names(merged_wip_) <- gsub("-|\\(|\\)", "__", names(merged_wip_))
# names(merged_wip_) <- gsub("\\$", "D", names(merged_wip_))
# names(merged_wip_) <- gsub("%", "Perc", names(merged_wip_))

merged_wip_test <-
  merged_wip_ %>% mutate(
    debt_cat = case_when(
      str_detect(Debt_Category, "Debt|Total|FGN") ~ Debt_Category,
      str_detect(Amount_Outstanding_in__USD, "[:alpha:]") ~ Amount_Outstanding_in__USD,
      str_detect(Unnamed__0.1, "D(ebt)|Total|FGN") ~ Unnamed__0.1
    ),
    amt_in_USD_inM = case_when(
      str_detect(Amount_Outstanding_in__USD, "[:alpha:]") &
        is.na(Amount_Outstanding_in__NGN) &
        is.na(Amount_Outstanding__in_NGN) ~ as.character(Amount_Outstanding_in_NGN),
      str_detect(Debt_Category, "[:alpha:]") &
        is.na(Amount_Outstanding_in__NGN) &
        is.na(Amount_Outstanding__in_NGN) &
        is.na(Unnamed__1) ~ Amount_Outstanding___USD__M__,
      str_detect(Debt_Category, "Grand-Total|Debt|Total") &
        is.na(Amount_Outstanding_in__NGN) &
        is.na(Amount_Outstanding__in_NGN) ~ Unnamed__1,
      str_detect(Amount_Outstanding_in__USD, "[:alpha:]") &
        is.na(Amount_Outstanding_in__NGN) ~ as.character(Amount_Outstanding__in_NGN),
      str_detect(Amount_Outstanding_in__USD, "[:alpha:]") ~ as.character(Amount_Outstanding_in__NGN),
      str_detect(Debt_Category, "Grand-Total|Debt|Total") ~ Amount_Outstanding_in__USD
      
    ),
    amt_in_NGN_inM = case_when(
      str_detect(Debt_Category, "Grand-Total|Debt|Total") &
        is.na(Amount_Outstanding_in__NGN) &
        is.na(Amount_Outstanding__in_NGN) ~ Amount_Outstanding_in_NGN,
      str_detect(Debt_Category, "Grand-Total|Debt|Total") &
        is.na(Amount_Outstanding_in__NGN) ~ Amount_Outstanding__in_NGN,
      str_detect(Debt_Category, "Grand-Total|Debt|Total") ~ Amount_Outstanding_in__NGN,
      str_detect(Amount_Outstanding_in__USD, "[:alpha:]") ~ as.double(Unnamed__3)
    )
  )
