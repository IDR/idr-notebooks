library(romero.gateway)

connection <- function() {
  # Disabling cluster until Tables are happy.
  # lastIP <- sample(5:10, 1) 
  lastIP <- '5'
  HOSTNAME <- paste0('10.0.48.', as.character(lastIP))
  USERNAME <- "public"
  PASSWORD <- "public"
  ome <- OMEROServer(host=HOSTNAME, port=as.integer(4064), username=USERNAME, password=PASSWORD)
  ome <- romero.gateway::connect(ome)
  return(ome)
}
