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
    name = "basic-auth"
  }

  data = {
    username = "myuser"
    password = "P4ssw0rd"
  }

  type = "kubernetes.io/basic-auth"
}

resource "kubernetes_deployment" "app" {
  metadata {
    name      = "loribooks-server"
    namespace = "fargate-node"
    labels    = {
      app = "loribooks"
    }
  }

  spec {
    replicas = 2

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
        init_container {
          image = "412299902699.dkr.ecr.us-east-1.amazonaws.com/loribooks:latest"
          name  = "makemigrations"

          env {
                name = "HOST"
                value = "lori-psql-db"
          }
          env {
              name="NAME"
              value="lori_assignemt"
          }
          # env {
          #   name="USER"
          #   value=resource.kubernetes_secret.lori_secret.data.username
          # }

          env {
            name="PORT"
            value="5432"
          }   

          # env {
          #     name="PASSWORD"
          #     value="${resource.kubernetes_secret.lori_secret.data.password}"
          # }
             
          env {
             name="NAME"
             value="lori_assignemt"
          }

          args = ["makemigrations"]
        }

        init_container {
          image = "412299902699.dkr.ecr.us-east-1.amazonaws.com/loribooks:latest"
          name  = "migrate"

          env {
                name = "HOST"
                value = "lori-psql-db"
          }
          env {
              name="NAME"
              value="lori_assignemt"
          }
          # env {
          #   name="USER"
          #   value=resource.kubernetes_secret.lori_secret.data.username
          # }

          env {
            name="PORT"
            value="5432"
          }   

          # env {
          #     name="PASSWORD"
          #     value=resource.kubernetes_secret.lori_secret.data.password
          # }
             
          env {
             name="NAME"
             value="lori_assignemt"
          }


          args = ["migrate"]
        }

        container {
          image = "412299902699.dkr.ecr.us-east-1.amazonaws.com/loribooks:latest"
          name  = "loribooks-server"

          port {
            container_port = 80
          }

          env {
                name = "HOST"
                value = "lori-psql-db"
          }
          env {
              name="NAME"
              value="lori_assignemt"
          }
          # env {
          #   name="USER"
          #   value="${resource.kubernetes_secret.lori_secret.data.username}"
          # }

          env {
            name="PORT"
            value="5432"
          }   

          # env {
          #     name="PASSWORD"
          #     value="${resource.kubernetes_secret.lori_secret.data.password}"
          # }
             
          env {
             name="NAME"
             value="lori_assignemt"
          }

          args = ["runserver"]
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
  }
  spec {
    selector = {
      app = "loribooks"
    }

    port {
      port        = 80
      target_port = 80
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
    }
    labels = {
        "app" = "loribooks"
    }
  }

  spec {
      backend {
        service_name = "loribooks-service"
        service_port = 80
      }
    rule {
      http {
        path {
          path = "/"
          backend {
            service_name = "loribooks-service"
            service_port = 80
          }
        }
      }
    }
  }

  depends_on = [kubernetes_service.app]
}