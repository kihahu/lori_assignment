variable "cluster_id" {
    description    =  "Put your cluster id here"
}

variable "vpc_id" {
  description      =  "put your vpc id"
}

variable "cluster_name" {
  description      =   "put your cluster name here"
}

variable "db_hostname" {
  description = "Postgres db hostname"
}

variable "private_subnets_cidr" {
  description = "Private cidrs"
}

variable "public_subnets_cidr" {
  description = "Public cidrs"
}

variable "db_password" {
  description = "Database password"
}
