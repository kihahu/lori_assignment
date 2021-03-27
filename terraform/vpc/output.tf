output "aws_subnets_public" {
  value   = aws_subnet.public.*.id
}

output "aws_subnets_private" {
  value   = aws_subnet.private.*.id
}

output "vpc_id" {
  value  = aws_vpc.main.id
}

output "db_subnet_group" {
  value = aws_db_subnet_group.default.name
}

output "lori_sns" {
  value = aws_sns_topic.lori_sns.arn
}
