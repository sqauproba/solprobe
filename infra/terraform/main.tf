terraform {
  required_version = ">= 1.5"
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "~> 5.0"
    }
  }
}

# Provisions managed Postgres and Redis for a SolProbe deployment.
# Adjust the provider block for your cloud of choice (AWS/Azure/GCP).

provider "google" {
  project = var.project
  region  = var.region
}

resource "google_sql_database_instance" "solprobe" {
  name             = "solprobe-db"
  database_version = "POSTGRES_16"
  region           = var.region

  settings {
    tier = "db-f1-micro"
  }
}

resource "google_redis_instance" "solprobe" {
  name           = "solprobe-redis"
  memory_size_gb = 1
  region         = var.region
}

output "database_connection_name" {
  value = google_sql_database_instance.solprobe.connection_name
}

output "redis_host" {
  value = google_redis_instance.solprobe.host
}
