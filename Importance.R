library(randomForestSRC)
data <- read.csv("data_nor.csv")
rownames(data) <- data[,1]
data <- data[,-1]
rfsrc_pbcmy <- rfsrc(Surv(OS.time, OS) ~ ., 
                     data = data, nsplit = 5,ntree = 300, 
                     na.action = "na.impute", tree.err = TRUE,  
                     importance = TRUE)
plot(rfsrc_pbcmy)
im <- as.data.frame(rfsrc_pbcmy$importance)
im <- as.data.frame(cbind(rownames(im),im))
colnames(im) <- c('Gene','Importance')
im$'normal' <- (im$Importance-min(im$Importance))/(max(im$Importance)-min(im$Importance))
im <- im[order(im$normal,decreasing = TRUE),]
write.csv(im,'importance.csv')