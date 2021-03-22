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
        container {
          image = "loribooks"
          name  = "loribooks-server"

          port {
            container_port = 80
          }

          env {
            HOST = "lori-psql-db"
            NAME = "lori_assignemt"
            USER = resource.kubernetes_secret.lori_secret.data.username
            PORT = "5432"
            PASSWORD = resource.kubernetes_secret.lori_secret.data.password
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