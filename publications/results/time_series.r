library(readr)
library(plotly)
library(dplyr)
library(reshape2)

df <- read.csv('Case 3_people_count.csv')


df_ach <- df %>% select(which(grepl('Zone_3', colnames(df)) & grepl('Chicago', colnames(df))))


df_ach <- select_if(df_ach, is.numeric)
if (nrow(df_ach) == 8760){
  v_time <- seq(ISOdatetime(2017,1,1,0,00,0), ISOdatetime(2017,12,31,23,50,0), by=(60*60))
  df_ach$Time <- v_time
} else{
  v_time <- seq(ISOdatetime(2017,1,1,0,00,0), ISOdatetime(2017,12,31,23,50,0), by=(60*10))
  df_ach$Time <- v_time
}

df_ach_sub <- df_ach %>% filter(Time >= ISOdatetime(2017,7,16,0,00,0) & Time < ISOdatetime(2017,7,21,0,00,0))

colnames(df_ach)





# Annual
p1_1 <- plot_ly(df_ach, x = ~Time, y = ~Solve_with_Temperature.Chicago.Zone_3_Ground_Truth,
                name = 'Ground truth', type = 'scatter', mode = 'lines',
                line = list(color='rgb(205,12,24)', width=2)) %>%
  add_trace(y = ~Solve_with_Temperature.Chicago.Zone_3_Hybrid_Solution, name = 'Solved with temperature', 
            line = list(color = 'rgb(22, 96, 167)', width = 2, dash = 'dash'))

p2_1 <- plot_ly(df_ach, x = ~Time, y = ~Solve_with_Humidity.Chicago.Zone_3_Ground_Truth,
                name = 'Ground truth', type = 'scatter', mode = 'lines',
                line = list(color='rgb(205,12,24)', width=2)) %>%
  add_trace(y = ~Solve_with_Humidity.Chicago.Zone_3_Hybrid_Solution, name = 'Solved with humidity ratio', 
            line = list(color = 'rgb(22, 96, 167)', width = 2, dash = 'dash'))

p3_1 <- plot_ly(df_ach, x = ~Time, y = ~Solve_with_CO2.Chicago.Zone_3_Ground_Truth,
                name = 'Ground truth', type = 'scatter', mode = 'lines',
                line = list(color='rgb(205,12,24)', width=2)) %>%
  add_trace(y = ~Solve_with_CO2.Chicago.Zone_3_Hybrid_Solution, name = 'Solved with humidity ratio', 
            line = list(color = 'rgb(22, 96, 167)', width = 2, dash = 'dash'))


# Week
p1_2 <- plot_ly(df_ach_sub, x = ~Time, y = ~Solve_with_Temperature.Chicago.Zone_3_Ground_Truth,
                name = 'Ground truth', type = 'scatter', mode = 'lines',
                line = list(color='rgb(205,12,24)', width=2)) %>%
  add_trace(y = ~Solve_with_Temperature.Chicago.Zone_3_Hybrid_Solution, name = 'Solved with temperature', 
            line = list(color = 'rgb(22, 96, 167)', width = 2, dash = 'dash')) 

p2_2 <- plot_ly(df_ach_sub, x = ~Time, y = ~Solve_with_Humidity.Chicago.Zone_3_Ground_Truth,
                name = 'Ground truth', type = 'scatter', mode = 'lines',
                line = list(color='rgb(205,12,24)', width=2)) %>%
  add_trace(y = ~Solve_with_Humidity.Chicago.Zone_3_Hybrid_Solution, name = 'Solved with humidity ratio', 
            line = list(color = 'rgb(22, 96, 167)', width = 2, dash = 'dash'))

p3_2 <- plot_ly(df_ach_sub, x = ~Time, y = ~Solve_with_CO2.Chicago.Zone_3_Ground_Truth,
                name = 'Ground truth', type = 'scatter', mode = 'lines',
                line = list(color='rgb(205,12,24)', width=2)) %>%
  add_trace(y = ~Solve_with_CO2.Chicago.Zone_3_Hybrid_Solution, name = 'Solved with humidity ratio', 
            line = list(color = 'rgb(22, 96, 167)', width = 2, dash = 'dash')) 

s1 <- subplot(p1_1, p2_1, p3_1, nrows = 3, shareX = TRUE, margin = 0.04, heights = c(0.33, 0.33, 0.33))
s2 <- subplot(p1_2, p2_2, p3_2, nrows = 3, shareX = TRUE, margin = 0.04, heights = c(0.33, 0.33, 0.33))

p <- subplot(s1, s2) %>% layout(showlegend = FALSE)

htmlwidgets::saveWidget(as_widget(p), 'uc3_occ.html')

