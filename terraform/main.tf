provider "aws" {
  region  = "us-east-1"
  profile = "default"
}

terraform {
  backend "s3" {
    encrypt = true
    bucket = "loribooks-terraform-state"
    region = "us-east-1"
    key = "terraform-state/terraform.tfstate"
  }
}

module "vpc" {
  source                     = "./vpc"
  environment                = var.environment
  vpc_cidr                   = var.vpc_cidr
  vpc_name                   = var.vpc_name
  cluster_name               = var.cluster_name
  public_subnets_cidr        = var.public_subnets_cidr
  availability_zones_public  = var.availability_zones_public
  private_subnets_cidr       = var.private_subnets_cidr
  availability_zones_private = var.availability_zones_private
  cidr_block-nat_gw          = var.cidr_block-nat_gw
  cidr_block-internet_gw     = var.cidr_block-internet_gw
}

module "eks" {
  source                        = "./eks"
  cluster_name                  = var.cluster_name
  environment                   = var.environment
  eks_node_group_instance_types = var.eks_node_group_instance_types
  private_subnets               = module.vpc.aws_subnets_private
  public_subnets                = module.vpc.aws_subnets_public
  fargate_namespace             = var.fargate_namespace
}

module "postgresql_rds" {
  source            = "github.com/azavea/terraform-aws-postgresql-rds"
  vpc_id            = module.vpc.vpc_id
  allocated_storage = "32"
  # engine_version = "12.5.R1"
  instance_type              = "db.t2.micro"
  storage_type               = "gp2"
  database_identifier        = "loribooks"
  database_name              = "lori_assignment"
  database_username          = "loribooks"
  database_password          = "f01931092903ff2ff308a0606bb87b201b6ba496"
  database_port              = "5432"
  backup_retention_period    = "30"
  backup_window              = "04:00-04:30"
  maintenance_window         = "sun:04:30-sun:05:30"
  auto_minor_version_upgrade = false
  multi_availability_zone    = true
  storage_encrypted          = false
  subnet_group               = "default-vpc-046da26edac788fc5"
  parameter_group            = "default.postgres11"
  monitoring_interval        = "60"
  deletion_protection        = true
  cloudwatch_logs_exports    = ["postgresql"]

  alarm_cpu_threshold         = "75"
  alarm_disk_queue_threshold  = "10"
  alarm_free_disk_threshold   = "5000000000"
  alarm_free_memory_threshold = "128000000"
  alarm_actions               = [module.vpc.lori_sns]
  ok_actions                  = [module.vpc.lori_sns]
  insufficient_data_actions   = [module.vpc.lori_sns]

  project     = "loribooks"
  environment = "dev"
}

module "kubernetes" {
  source       = "./kubernetes"
  cluster_id   = module.eks.cluster_id
  vpc_id       = module.vpc.vpc_id
  cluster_name = module.eks.cluster_name
  db_hostname  = module.postgresql_rds.hostname
}
