#install.packages("E:\\NCSU\\Semester 1\\Automated Learning and Data Analysis\\Project\\Enron\\e1071_1.6-7.zip", repos = NULL, type="source")

library(e1071)
locations_path = file.choose()
dat <- read.csv(locations_path, header = TRUE);
date<-strptime(dat[,4],format='%d %b %Y %H:%M:%S %z')
data<-data.frame(dat[,1],date,dat[,2])
model<-naiveBayes(data[,1:2],data[,3])
pred<-predict(model, data[6,2])


#install.packages("igraph")
library(igraph)

#edges<-data.frame(data[,1],data[,3])
#attach(edges)
#tapply(data[,3],data[,1],unique)


#g <- graph.data.frame( edges )
#adjlist <- get.adjedgelist(g)

#Making Adjacency Matrix
m <- as.matrix(data[,c(1,3)])
el <- cbind(m[, 1], c(m[, -1]))
adj_list<-get.adjacency(graph.edgelist(el),sparse=FALSE)

#Plotting graph
g <- graph.adjacency(adj_list, weighted=T, mode = 'directed')
set.seed(3952)
layout1 <- layout.fruchterman.reingold(g)
plot(g, layout=layout1)
tkplot(g, layout=layout.kamada.kawai)
V(g)$label.cex <- 2.2 * V(g)$degree / max(V(g)$degree)+ .2
V(g)$label.color <- rgb(0, 0, .2, .8)
V(g)$frame.color <- NA
egam <- (log(E(g)$weight)+.4) / max(log(E(g)$weight)+.4)
E(g)$color <- rgb(.5, .5, 0, egam)
E(g)$width <- egam
# plot the graph in layout1
plot(g, layout=layout1)

bsk<-data[,c(1,3)]
bsk.network<-graph.data.frame(bsk, directed=T)
V(bsk.network)
E(bsk.network)
degree(bsk.network)
plot(bsk.network)

#install.packages('statnet')
library(sna)
gbn<-bn(adj_list,param.fixed=list(pi=0,sigma=0,rho=0))
summary(gbn)
plot(gbn)

library(proxy)
ls('package:proxy')
predval<-dist(adj_list)
adjmatrix<-(as.matrix(predval)>2)
diag(adjmatrix)<-FALSE
adjmatrix[adjmatrix==TRUE]<-1
adjmatrix[lower.tri(adjmatrix)] <- 0
might<-graph.adjacency(adjmatrix)