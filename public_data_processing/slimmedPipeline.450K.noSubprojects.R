# Marc Jan Bonder
# m.j.bonder @ umcg.nl
#
############################
# Release data: 18-04-2016 #
############################

##############################
###### VARIABLES TO SET ######
##############################
#
### PATHs to files and folders
#set working directory (If necessary)
packages_path="/data/p283190/r_packages_methylation" # peregrine
# packages_path="/groups/umcg-wijmenga/tmp04/projects/2019-comethylationnetwork/tools/r_packages/"
# if (!requireNamespace("BiocManager", quietly = TRUE))
#     install.packages("BiocManager", lib=packages_path)
# BiocManager::install("lumi", lib=packages_path)
# BiocManager::install("methylumi", lib=packages_path)
# BiocManager::install("minfi", lib=packages_path)
# BiocManager::install("wateRmelon", lib=packages_path)

.libPaths(packages_path)
require('lumi')
require('methylumi')
require('minfi')
require('wateRmelon')
# setwd("/groups/umcg-wijmenga/tmp04/projects/2019-comethylationnetwork/publicdata/GEO/downloadAndPreProcessing/code/450K_DataProcessing")
#
# If working on Windows set this:
# memory.limit(3000)
#

args <- commandArgs(trailingOnly = TRUE)
cat(args, sep = "\n")

if (length(args)<3) {
  print(paste("Found args: ",length(args)))

  stop("Usage: datainputfolder outputfolder name", call.=FALSE)
}

# set PATH to results folder
PATH_RES <-  args[2] #"/hps/nobackup/stegle/users/mjbonder/tools/450K_Processing/Res450/"
#
# set PATH to a folder of "projects" where each project corresponds to a folder of 450K plate extracted data, in .idat format.
PATH_PROJECT_DATA <- args[1] #"./DATA/"
#
## set PATH to the file with frequent SNP informations, on which SNP filtering is based. If = NULL, no probe removed. Can handle arrays of filenames.
# PATH_ProbeSNP_LIST <- c("/groups/umcg-wijmenga/tmp04/projects/2019-comethylationnetwork/publicdata/GEO/downloadAndPreProcessing/code/450K_DataProcessing/ADDITIONAL_INFO/ProbeFiltering/freq5percent/probeToFilter_450K_1000G_omni2.5.hg19.EUR_alleleFreq5percent_50bp_wInterroSite.txt",
# "/groups/umcg-wijmenga/tmp04/projects/2019-comethylationnetwork/publicdata/GEO/downloadAndPreProcessing/code/450K_DataProcessing/ADDITIONAL_INFO/ProbeFiltering/ProbesBindingNonOptimal/Source&BSProbesMappingMultipleTimesOrNotBothToBSandNormalGenome.txt")
PATH_ProbeSNP_LIST <- c("/home/p283190/450K_DataProcessing/ADDITIONAL_INFO/ProbeFiltering/freq5percent/probeToFilter_450K_1000G_omni2.5.hg19.EUR_alleleFreq5percent_50bp_wInterroSite.txt",
"/home/p283190/450K_DataProcessing/ADDITIONAL_INFO/ProbeFiltering/ProbesBindingNonOptimal/Source&BSProbesMappingMultipleTimesOrNotBothToBSandNormalGenome.txt")


#PATH_ProbeSNP_LIST <- c("./ADDITIONAL_INFO/ProbeFiltering/freq1percent/probeToFilter_450K_GoNL.hg19.ALL_alleleFreq1percent.txt", "./ADDITIONAL_INFO/ProbeFiltering/ProbesBindingNonOptimal/Source&BSProbesMappingMultipleTimesOrNotBothToBSandNormalGenome.txt")
#PATH_ProbeSNP_LIST <- c("./ADDITIONAL_INFO/ProbeFiltering/freq1percent/probeToFilter_450K_EnsembleV70&GoNL.hg19.ALL_alleleFreq1percent.txt", "./ADDITIONAL_INFO/ProbeFiltering/AutosomeAndSnpProbes.txt", "./ADDITIONAL_INFO/ProbeFiltering/ProbesBindingNonOptimal/Source&BSProbesMappingMultipleTimesOrNotBothToBSandNormalGenome.txt")
#PATH_ProbeSNP_LIST <- NULL
#
# The name that will be given to result files
projectName = args[3] # "ILLUMINA450K_IPSc"
#
#Set number of cores to use in multi-threading.
coresMultiThread = 8;
Sys.setenv("MC_CORES"=coresMultiThread)
mc.cores=8
#
##############################################
#####  NOW YOU CAN SOURCE THIS SCRIPT !  #####
##############################################
#####
#####
##############################################
###### source scripts and load libraries #####
##############################################

coresMultiThread = 4;

{
  if(is.character(PATH_ProbeSNP_LIST)){
    if(length(PATH_ProbeSNP_LIST)==1){
      probeSNP_LIST <- unlist(read.table(file=PATH_ProbeSNP_LIST, quote="", sep="\t", header=TRUE))
    } else {
      probeSNP_LIST <- NULL
      for(id in 1:length(PATH_ProbeSNP_LIST)){
        probeSNP_LIST <- union(probeSNP_LIST, unlist(read.table(file=PATH_ProbeSNP_LIST[id], quote="", sep="\t", header=TRUE)))
      }
    }
  }
  else{
    probeSNP_LIST <- NULL
  }
}


subProjects <- dir(PATH_PROJECT_DATA)

unMeth <- NULL
meth <- NULL

#for all subprojects
for(i in 1:length(subProjects)){

# for(i in 1:1) {
  start_time <- Sys.time()
  projectName_batch <- subProjects[i]
  sampleTable <- dir(paste(PATH_PROJECT_DATA, projectName_batch, "/", sep=""), pattern="TableSample")
  # cat(sampleTable)
  controlTable <- dir(paste(PATH_PROJECT_DATA, projectName_batch, "/", sep=""), pattern="TableControl")
  # cat("Processing sub-project: ", projectName_batch, "\n")


  #####
  if(length(sampleTable) < 1 && length(controlTable) < 1 && length(list.files(paste(PATH_PROJECT_DATA, projectName_batch, "/", sep="/"), pattern=".idat"))>0){

    barcode<- list.files(paste(PATH_PROJECT_DATA, projectName_batch, "/", sep="/"), pattern=".idat")

    barcode <- gsub("_Grn","",x=barcode)
    barcode <- gsub("_Red","",x=barcode)
    barcode <- unique(barcode)
    cat(barcode)

    if(length(barcode)<2){
      cat("\n\tSkipped folder: ",projectName_batch,"\n")
      cat("\t to little samples")
      next;
    }

    cat("\n\tStart data loading...\n")
    methLumi_dataTmpData <- methylumIDAT(barcode, idatPath=paste(PATH_PROJECT_DATA, projectName_batch, "/", sep="/"), parallel=T, mc.cores = coresMultiThread, n=T)

    #methLumi_dataTmpData <- as(methLumi_dataTmpData, 'MethyLumiM')

    cat("\tProject sample nb: ", length(barcode), ".\n")
    cat("\tData dimensions: ", dim(methLumi_dataTmpData)[1],"x", dim(methLumi_dataTmpData)[2], ".\n")
    cat("\t...data loaded..\n\n")

    #############################
    # starts data preprocessing #
    #############################

    indexProbe2remove <- which(is.element(featureNames(methLumi_dataTmpData), probeSNP_LIST))
    if(length(indexProbe2remove)>0) methLumi_dataTmpData <- methLumi_dataTmpData[-indexProbe2remove,]

    if(is.null(methLumi_dataTmpData)){
      next;
    }

  } else {
    next;
  }

  ################################################
  # Sub-project data & information concatenation #
  ################################################

  if(is.null(unMeth) && length(sampleNames(methLumi_dataTmpData))>0){
    unMeth <- unmethylated(methLumi_dataTmpData)
    meth <- methylated(methLumi_dataTmpData)

    cat("\t Chanels plate", i, " ok (", dim(unMeth)[1], "x", dim(unMeth)[2], ").\n")

    #select "useful" probe annotations
    rm(methLumi_dataTmpData)

  } else if(length(sampleNames(methLumi_dataTmpData))>0){
    print(dim(methLumi_dataTmpData))
    #concatenate 'chanels'

    if(length(rownames(meth)) == length(rownames(methylated(methLumi_dataTmpData))) && all(rownames(meth) == rownames(methylated(methLumi_dataTmpData)))){
      meth <- cbind(meth, methylated(methLumi_dataTmpData))
      unMeth <- cbind(unMeth, unmethylated(methLumi_dataTmpData))
    } else {
      unMeth_i <- unmethylated(methLumi_dataTmpData)
      meth_i <- methylated(methLumi_dataTmpData)

      unMeth_i<- as.matrix(unMeth_i[which(rownames(unMeth_i) %in% rownames(unMeth)),])
      meth_i<- as.matrix(meth_i[which(rownames(meth_i) %in% rownames(meth)),])

      unMeth<- as.matrix(unMeth[which(rownames(unMeth) %in% rownames(unMeth_i)),])
      meth<- as.matrix(meth[which(rownames(meth) %in% rownames(meth_i)),])

      meth <- cbind(meth[order(rownames(meth)),], meth_i[order(rownames(meth_i)),])
      unMeth <- cbind(unMeth[order(rownames(unMeth)),], unMeth_i[order(rownames(unMeth_i)),])

      rm(unMeth_i)
      rm(meth_i)
    }

    cat("\t Chanels ok (", dim(unMeth)[1], "x", dim(unMeth)[2], ").\n")
  }
  end_time = Sys.time()
  cat("Eash sample takes:", end_time-start_time, "sec")
}
if(is.null(unMeth) || is.null(meth)){
  stop()
}



#split out over: Type I U / Type I M /  Type II U / Type II M
hm450.ordering <- hm450.ordering[which(rownames(hm450.ordering)%in%rownames(unMeth)),]
hm450.ordering <- hm450.ordering[order(rownames(hm450.ordering)),]


write.table(unMeth[intersect(which(hm450.ordering$DESIGN=="I"),which(hm450.ordering$COLOR_CHANNEL=="Red")),], file=paste(PATH_RES, projectName, "_T1_Red_U_Signal.txt", sep=""), quote=FALSE, sep="\t", col.names = NA)
write.table(meth[intersect(which(hm450.ordering$DESIGN=="I"),which(hm450.ordering$COLOR_CHANNEL=="Red")),], file=paste(PATH_RES, projectName, "_T1_Red_M_Signal.txt", sep=""), quote=FALSE, sep="\t", col.names = NA)
write.table(unMeth[intersect(which(hm450.ordering$DESIGN=="I"),which(hm450.ordering$COLOR_CHANNEL=="Grn")),], file=paste(PATH_RES, projectName, "_T1_Grn_U_Signal.txt", sep=""), quote=FALSE, sep="\t", col.names = NA)
write.table(meth[intersect(which(hm450.ordering$DESIGN=="I"),which(hm450.ordering$COLOR_CHANNEL=="Grn")),], file=paste(PATH_RES, projectName, "_T1_Grn_M_Signal.txt", sep=""), quote=FALSE, sep="\t", col.names = NA)
write.table(unMeth[which(hm450.ordering$DESIGN=="II"),], file=paste(PATH_RES, projectName, "_T2_U_Signal.txt", sep=""), quote=FALSE, sep="\t", col.names = NA)
write.table(meth[which(hm450.ordering$DESIGN=="II"),], file=paste(PATH_RES, projectName, "_T2_M_Signal.txt", sep=""), quote=FALSE, sep="\t", col.names = NA)

