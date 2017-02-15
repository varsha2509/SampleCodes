#### Sample code snippets in R. 
#The following code contains examples for performing robust regression on a dataset, coding of categorical data
# and some basic plots using ggplot2
#Author: Varsha Gopalakrishnan
#############################

#Read dataset
setwd("C:/Users/Varsha/OneDrive/Documents/OSU-CHBE/Spring 2014/STAT 6450/Project3");
reg.data = read.csv("Data.csv", header = T)

#Summarize dataset
summary(reg.data)

list.na<-is.na(reg.data)
list.nomissing <-rowSums(list.na)==0
reg.data.valid<-reg.data[list.nomissing,]
summary(reg.data.valid)
#Read different column vectors and store it in variables
Site = reg.data.valid$SITE
gen = reg.data.valid$CSEX
MVPA = reg.data.valid$MMVPACG3;
PA = sqrt(MVPA)
AVG = reg.data.valid$AVGTP;
A = log(AVG)
ITNR = reg.data.valid$INCNTM;
BMI = reg.data.valid$BMIPG3;
RACE = reg.data.valid$CRACE
Site = reg.data.valid$SITE
gen = reg.data.valid$CSEX
WL = reg.data.valid$WJPCSCG3;


 
#Robust regression
library(MASS)
RReg = rlm(AVG ~ MVPA)
summary(RReg)

#Robust regression -> Huber weights
rr.huber = rlm(AVG ~ MVPA + BMI + ITNR + gen + RACE , data = reg.data.valid)
summary(rr.huber)
hweights = data.frame(Site = Site , resid = rr.huber$resid , weights = rr.huber$w)
hweights2 = hweights[order(rr.huber$w),]
hweights2[1:733,]


#Robust regression fit
Fit_R = lm(AVG ~ MVPA+ BMI + ITNR + gen + RACE , weights= (1/MVPA), data=reg.data.valid)
summary(Fit_R)

plot(Fit_R)

step(Fit_R)

Data = data.frame(reg.data)

##Coding of categorical variables
reg.data.valid$CSEX.f = factor(reg.data.valid$CSEX, labels=c("Male","Female"))
contr.treatment(2)
contrasts(reg.data.valid$CSEX.f) = contr.treatment(2)
print(reg.data.valid$CSEX.f)
summary(lm(reg.data.valid$AVG ~ reg.data.valid$CSEX.f, data=reg.data.valid))



#Coding of categorical variables - Race
reg.data.valid$CRACE.f = factor(reg.data.valid$CRACE, labels = c("American Indian","Asian","Black","White","Other"))

contrasts(reg.data.valid$CRACE.f) = contr.treatment(5)
summary(lm(reg.data.valid$AVG ~reg.data.valid$CRACE.f , data=reg.data.valid))
print(reg.data.valid$CRACE.f)


#Coding of categorical variable for SITE
reg.data.valid$SITE.f = factor(reg.data.valid$Site, labels = c("1","2","3","4","5","6","7","8","0"))


## ANOVA test on full and reduced model
full.model = lm(reg.data.valid$AVG ~ MVPA + BMI + Site + RACE + ITNR + gen, data = reg.data.valid )
reduced.model = lm(reg.data.valid$AVG ~ MVPA + BMI + Site  + ITNR + RACE, data = reg.data.valid)
anova(full.model, reduced.model)



################ Plotting in R using ggplot2
#install ggplot2 package
#install.packages("ggplot2")

library(ggplot2)

#Set working directory as the location where your files are stored

###%%%%&&&&###### Change this line to your working directory:
setwd("C:/Users/Varsha/OneDrive/Documents/OSU-CHBE/Spring 2016/ggplotIntro")

## Reading files - .txt or .csv or .Rdata format
data = read.csv('BiodieselResults.csv', header= TRUE, na.string = "Nan")

#Basic bar plots
ggplot(data, aes(x=Source, y=Value)) + 
  geom_bar(stat='identity', aes(fill=(Emissions)))


#Changing colors and adding labels to your plot
#(Plot a)
a = ggplot(data, aes(x=Source, y=Value)) + 
  geom_bar(stat='identity', aes(fill=(Emissions))) +  
  scale_fill_manual(values=c('#FF0000','#800000', '#8DD35F')) +
  theme_bw() +
  xlab('Source of emissions') +
  ylab('kg of pollutant')


#Changing the same plot to a log plot on the y axis
# (Plot b)
b = ggplot(data, aes(x=Source, y=Value)) + 
  geom_bar(stat='identity', aes(fill=(Emissions))) +  
  scale_fill_manual(values=c('#FF0000','#800000', '#8DD35F')) +
  theme_bw() +
  xlab('Source of emissions') +
  ylab('kg of pollutant') + 
  scale_y_log10()



#Re-ordering data by creating categorical variables
data$Emissions = factor(data$Emissions, levels = c('PM10', 'SO2', 'CO2'),
                        ordered = TRUE)
data$Source = factor(data$Source, levels = c('CHP', 'Biodiesel'),
                     ordered = TRUE)



#Plot with reordered data
#(Plot c)
c = ggplot(data, aes(x=Source, y=Value)) + 
  geom_bar(stat='identity', aes(fill=(Emissions))) +  
  scale_fill_manual(values=c('#FF0000','#800000', '#8DD35F')) +
  theme_bw() +
  xlab('Source of emissions') +
  ylab('kg of pollutant')


#Changing font size, relocating legend, adding title to your plot
#(Plot d)
d = ggplot(data, aes(x=Source, y=Value)) + 
  geom_bar(stat='identity', aes(fill=(Emissions))) +  
  scale_fill_manual(values=c('#FF0000','#800000', '#8DD35F')) +
  theme_bw() +
  xlab('Source of emissions') +
  ylab('kg of pollutant') + 
  theme(axis.title.x = element_text(size = rel(1.5)),
        axis.text.x = element_text(size = rel(1.2)),
        axis.title.y = element_text(size = rel(1.5)),
        axis.text.y = element_text(size = rel(1.2)),                            
        legend.text = element_text(size = rel(1.25)), 
        legend.position = 'bottom') + 
  ggtitle("My first plot") + 
  theme(plot.title = element_text(lineheight=1.2, face="bold"))




##Multi plot function


######### Global multi plot function #######
# Multiple plot function
#
# ggplot objects can be passed in ..., or to plotlist (as a list of ggplot objects)
# - cols:   Number of columns in layout
# - layout: A matrix specifying the layout. If present, 'cols' is ignored.
#
# If the layout is something like matrix(c(1,2,3,3), nrow=2, byrow=TRUE),
# then plot 1 will go in the upper left, 2 will go in the upper right, and
# 3 will go all the way across the bottom.
#
multiplot <- function(..., plotlist=NULL, file, cols=1, layout=NULL) {
  library(grid)
  
  # Make a list from the ... arguments and plotlist
  plots <- c(list(...), plotlist)
  
  numPlots = length(plots)
  
  # If layout is NULL, then use 'cols' to determine layout
  if (is.null(layout)) {
    # Make the panel
    # ncol: Number of columns of plots
    # nrow: Number of rows needed, calculated from # of cols
    layout <- matrix(seq(1, cols * ceiling(numPlots/cols)),
                     ncol = cols, nrow = ceiling(numPlots/cols))
  }
  
  if (numPlots==1) {
    print(plots[[1]])
    
  } else {
    # Set up the page
    grid.newpage()
    pushViewport(viewport(layout = grid.layout(nrow(layout), ncol(layout))))
    
    # Make each plot, in the correct location
    for (i in 1:numPlots) {
      # Get the i,j matrix positions of the regions that contain this subplot
      matchidx <- as.data.frame(which(layout == i, arr.ind = TRUE))
      
      print(plots[[i]], vp = viewport(layout.pos.row = matchidx$row,
                                      layout.pos.col = matchidx$col))
    }
  }
}

multiplot(a,b,c,d,cols=2)


