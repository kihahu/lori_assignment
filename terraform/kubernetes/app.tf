data "aws_subnet_ids" "all" {
  vpc_id = var.vpc_id
}

resource "kubernetes_namespace" "fargate" {
  metadata {
    labels = {
      app = "loribooks"
    }
    name = "fargate-node"
  }
}

resource "kubernetes_secret" "lori_secret" {
  metadata {
    name      = "lori-db-credentials"
    namespace = kubernetes_namespace.fargate.metadata.0.name
  }

  data = {
    username = "loribooks"
    password = var.db_password
  }

  type = "kubernetes.io/basic-auth"
}

resource "kubernetes_deployment" "app" {
  metadata {
    name      = "loribooks-server"
    namespace = "fargate-node"
    labels = {
      app = "loribooks"
    }
  }

  spec {
    replicas = 3

    selector {
      match_labels = {
        app = "loribooks"
      }
    }

    template {
      metadata {
        labels = {
          app = "loribooks"
        }
      }

      spec {

        container {
          image = "412299902699.dkr.ecr.us-east-1.amazonaws.com/loribooks:latest"
          name  = "loribooks-server"

          port {
            container_port = 8000
          }

          env {
            name  = "HOST"
            value = var.db_hostname
          }

          env {
            name = "USER"
            value_from {
              secret_key_ref {
                key  = "username"
                name = kubernetes_secret.lori_secret.metadata.0.name
              }
            }
          }

          env {
            name  = "PORT"
            value = "5432"
          }

          env {
            name = "PASSWORD"
            value_from {
              secret_key_ref {
                key  = "password"
                name = kubernetes_secret.lori_secret.metadata.0.name
              }
            }
          }

          env {
            name  = "NAME"
            value = "lori_assignment"
          }

          liveness_probe {
            exec {
              command = ["curl http://b69ee518-fargatenode-lorib-be0e-1165705763.us-east-1.elb.amazonaws.com/"]
            }
            initial_delay_seconds = 3
            period_seconds        = 3
          }
        }
      }
    }
  }
  depends_on = [kubernetes_namespace.fargate]

}

resource "kubernetes_service" "app" {
  metadata {
    name      = "loribooks-service"
    namespace = "fargate-node"
    annotations = {
      "alb.ingress.kubernetes.io/subnets" = jsonencode(data.aws_subnet_ids.all.ids)
    }
  }
  spec {
    selector = {
      app = "loribooks"
    }

    port {
      port        = 8000
      target_port = 8000
      protocol    = "TCP"
    }

    type = "NodePort"
  }

  depends_on = [kubernetes_deployment.app]
}

resource "kubernetes_ingress" "app" {
  metadata {
    name      = "loribooks-lb"
    namespace = "fargate-node"
    annotations = {
      "kubernetes.io/ingress.class"           = "alb"
      "alb.ingress.kubernetes.io/scheme"      = "internet-facing"
      "alb.ingress.kubernetes.io/target-type" = "ip"
      "alb.ingress.kubernetes.io/subnets" = jsonencode(data.aws_subnet_ids.all.ids)
    }
    labels = {
      "app" = "loribooks"
    }
  }

  spec {
    backend {
      service_name = "loribooks-service"
      service_port = 8000
    }
    rule {
      http {
        path {
          path = "/"
          backend {
            service_name = "loribooks-service"
            service_port = 8000
          }
        }
      }
    }
  }

  depends_on = [kubernetes_service.app]
}
