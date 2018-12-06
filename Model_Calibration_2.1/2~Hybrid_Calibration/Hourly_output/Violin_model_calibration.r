library(readr)
library(plotly)
library(dplyr)
library(reshape2)


filename <- "hourly_conusmption.csv"
filename <- "People_count_with_CO2.csv"

df <- read.csv(filename)

df_melt <- df %>% melt

View(df_melt)

table(df_melt$variable)


df_melt_raw <- df_melt %>% mutate(Trace = case_when((grepl('Ground.Truth', variable)) ~ 'Ground Truth',
                                                    (grepl('Inverse.Solution', variable)) ~ 'Inverse Solution',
                                                    (grepl('Normal.Simulation', variable)) ~ 'Normal Simulation'),
                                  Zone = case_when(grepl('BACK', variable) ~ 'Zone Back',
                                                   grepl('LEFT', variable) ~ 'Zone Left',
                                                   grepl('RIGHT', variable) ~ 'Zone Right',
                                                   grepl('FRONT', variable) ~ 'Zone Front',
                                                   grepl('CORE', variable) ~ 'Zone Core')) %>%
  filter(!is.na(Trace))


View(df_melt_raw)

df_melt_raw <- df_melt_raw[which(df_melt_raw$Zone != 'Zone Core'),]

p <- ggplot(df_melt_raw, aes(x = Trace, y = value, fill = Trace)) + 
  geom_violin(trim= TRUE)+
  facet_wrap(~ Zone) +
  labs(title = paste0("Zone People Count (except core zone)"))+
  theme_bw() +
  theme(plot.title=element_text(size=16, face="bold", hjust = 0.5),
        plot.subtitle=element_text(size=14, hjust=0.5, face="italic", color="black"))+
  theme(axis.title.x=element_blank(),
        axis.text.x=element_blank(),
        axis.ticks.x=element_blank())
p


