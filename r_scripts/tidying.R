library(tidyverse)
library(data.table)






map_df_fread <- function(path, pattern = "*.csv") {
  list.files(path, pattern, full.names = TRUE) %>% 
    map_df(~fread(.))
}

DATA_F <- map_df_fread('scrapper/downloads/')




