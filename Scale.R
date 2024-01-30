data <- read.csv("data_tcga.csv")
for (i in 4:56)
{
  data[,i] <- scale(data[,i])
}
write.csv(data,'data_nor.csv')