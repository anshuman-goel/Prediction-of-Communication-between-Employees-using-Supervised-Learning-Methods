#Loading Library
install.packages("e1071")
install.packages("gsubfn")
install.packages("igraph")
install.packages("sna")
install.packages("proxy")
library("e1071")
library("gsubfn")
library("igraph")
library("sna")
library("proxy")

#Processing for bagging
#Loading the dataset
#locations_path = file.choose()
dat <- read.csv("./email_processed.csv", header = FALSE,sep = '|',quote = "");

#Reading in Date Format
date<-strptime(dat[,3],format=' %a, %d %b %Y %H:%M:%S %z')

dat$V3 = gsub('.*\\s(\\w+\\s\\d+)\\s.*','\\1', dat$V3) #reduce to month and year

dat2 = subset(dat, grepl("(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\\s\\d{4}",dat$V3)) #remove values with nonconforming format after processing

dates = sort(unique(dat2$V3)) #unique dates to be used in bins)
            
#</EndProcessing>

for(l in 1:length(dates))
{
  curDate = subset(dat2,dat2$V3==dates[l])
  
  #Building new corrected data frame
  data<-data.frame(curDate$V1,curDate$V3,curDate$V2)
  
  #Sampling Data
  train <- data[sample(seq_len(nrow(data)), size = nrow(data)*.4), ]
  test<-data[-as.numeric(row.names(train)),]
  test <- test[sample(seq_len(nrow(test)), nrow(data)*.2), ]
  
  #Making Adjacency Matrix of Training data
  m <- as.matrix(train[,c(1,3)])
  adj_list<-get.adjacency(graph.edgelist(cbind(m[, 1], c(m[, -1]))),sparse=FALSE)
  
  #Plotting graph
  g <- graph.adjacency(adj_list, weighted=T, mode = 'directed')
  set.seed(395452)
  layout1 <- layout.fruchterman.reingold(g)
  
  #Predicting the most probable edges
  #Calculaing the distance
  predval<-dist(adj_list)
  adjmatrix<-(as.matrix(predval)>=1)
  
  #Initailizing variables for calculating accuracy
  correct<-0
  count<-0
  
  #Testing the Model
  for(i in 1:nrow(adjmatrix))
  {
    for(j in 1:ncol(adjmatrix))
    {
      if(adjmatrix[i,j]==TRUE)
      {
        for(k in 1:nrow(test))
        {
          if((rownames(adjmatrix)[i]==test[k,1] && colnames(adjmatrix)[j]==test[k,3]))
          {
            correct<-correct+1
          }
        }
        count<-count+1
      }
    }
  }
  print(dates[l])
  print(c('Accuracy is (as per predicted in adjacency matrix):',correct*2/count))
  print(c('Accuracy is (tuples predicted in test data):',correct/nrow(test)))
}
