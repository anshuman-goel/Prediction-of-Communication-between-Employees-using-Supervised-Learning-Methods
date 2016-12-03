##############################################################################
#
# Social Network Prediction on Enron Email dataset
# CSC-522 Project
#
# By:
# Anshuman Goel - agoel5
# Rohit Nambisam - rnambis
# Tyler Cannon - tjcannon
#
##############################################################################

#Installing Naive Bayesian Package e1071 saved on local machine

install.packages("E:\\NCSU\\Semester 1\\Automated Learning and Data Analysis\\Project\\Enron\\e1071_1.6-7.zip", repos = NULL, type="source")

#Installing Package
install.packages("igraph")

#Installing packages for graph links prediction 
#Considering proxy package is already installed
install.packages('statnet')

#Loading Library
library(e1071)

#Loading the dataset
dat <- read.csv('E:\\NCSU\\Semester 1\\Automated Learning and Data Analysis\\Project\\Enron\\SocialNetwork\\email_processed.csv', header = FALSE,sep = '|',quote = "");

#Reading in Date Format
date<-strptime(dat[,3],format=' %a, %d %b %Y %H:%M:%S %z')

#Building new corrected data frame
data<-data.frame(dat[,1],date,dat[,2])
rm(dat)

#Sampling Data
set.seed(123456)
train <- data[sample(seq_len(nrow(data)), size = 1000), ]
test<-data[-as.numeric(row.names(train)),]
test <- test[sample(seq_len(nrow(test)), size = 300), ]

#To freeup RAM
rm(data)

#Building Naive Bayesian Model on training data
model<-naiveBayes(train[,1],train[,3])

#Initializing variable
correct_nb<-0

#Testing model with test data and Calculating Accuracy
for (i in 1:nrow(test)) {
  pred<-predict(model, test[i,1])
  if(pred==test[i,3])
    correct_nb<-correct_nb+1
}

#Accuracy of Naive Bayesian Model
no_rows<-nrow(test)
print(c('Accuracy of Naive Bayesian Model is : ',correct_nb/no_rows))

#Removing Variables
rm(i,pred,model)

#Loading the igraph library
library(igraph)

#Making Adjacency Matrix of Training data
m <- as.matrix(train[,c(1,3)])
adj_list<-get.adjacency(graph.edgelist(cbind(m[, 1], c(m[, -1]))),sparse=FALSE)

#Plotting graph
g <- graph.adjacency(adj_list, weighted=T, mode = 'undirected')
set.seed(395452)
layout1 <- layout.fruchterman.reingold(g)

#Different and interactive type of graph
tkplot(g, layout=layout.kamada.kawai)

#Removing unnecessary variables
rm(g,layout1)

#Loading libraries
library(sna)
library(proxy)

#Predicting the most probable edges
#Calculaing the distance
predval<-dist(adj_list)
adjmatrix<-(as.matrix(predval)>1.5)

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

print(c('Accuracy of Naive Bayesian Model is : ',correct_nb/no_rows))
print(c('Accuracy is (as per predicted in adjacency matrix):',correct*2/count))
print(c('Accuracy is (tuples predicted in test data):',correct/nrow(test)))