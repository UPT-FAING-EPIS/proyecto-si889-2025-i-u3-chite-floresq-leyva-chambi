terraform {
  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = ">= 4.0.0"
    }
  }
}

provider "azurerm" {
  features {}

  subscription_id = var.subscription_id
  client_id       = var.client_id
  client_secret   = var.client_secret
  tenant_id       = var.tenant_id
}

# Grupo de recursos
resource "azurerm_resource_group" "rg_proyecto_patrones" {
  name     = "rg-proyecto-patrones-u2"
  location = "East US 2"
}

# Servidor SQL
resource "azurerm_mssql_server" "server_proyecto_patrones" {
  name                         = "server-proyecto-patrones-u2"
  resource_group_name          = azurerm_resource_group.rg_proyecto_patrones.name
  location                     = azurerm_resource_group.rg_proyecto_patrones.location
  version                      = "12.0"
  administrator_login          = var.sqladmin_username
  administrator_login_password = var.sqladmin_password

  identity {
    type = "SystemAssigned"
  }
}

# Base de datos única: DocMark
resource "azurerm_mssql_database" "db_docmark" {
  name                        = "DocMark"
  server_id                   = azurerm_mssql_server.server_proyecto_patrones.id
  sku_name                    = "GP_S_Gen5_1"
  collation                   = "SQL_Latin1_General_CP1_CI_AS"
  auto_pause_delay_in_minutes = 30
  min_capacity                = 0.5
  max_size_gb                 = 32
  storage_account_type        = "Local"
}

# Regla de firewall para permitir acceso desde Azure
resource "azurerm_mssql_firewall_rule" "allow_azure_services" {
  name             = "AllowAzureServices"
  server_id        = azurerm_mssql_server.server_proyecto_patrones.id
  start_ip_address = "0.0.0.0"
  end_ip_address   = "255.255.255.255"
}

# Plan de App service
resource "azurerm_service_plan" "app_plan_proyecto_patrones" {
  name                = "app-plan-proyecto-patrones-u2"
  location            = azurerm_resource_group.rg_proyecto_patrones.location
  resource_group_name = azurerm_resource_group.rg_proyecto_patrones.name
  os_type             = "Linux"
  sku_name            = "B1"
}

# Aplicación Web para FastAPI 
resource "azurerm_linux_web_app" "webapp_proyecto_patrones" {
  name                = "webapp-proyecto-patrones-u2"
  location            = azurerm_resource_group.rg_proyecto_patrones.location
  resource_group_name = azurerm_resource_group.rg_proyecto_patrones.name
  service_plan_id     = azurerm_service_plan.app_plan_proyecto_patrones.id

  site_config {
    application_stack {
      python_version = "3.10"
    }
  }

  app_settings = {
    "WEBSITES_ENABLE_APP_SERVICE_STORAGE" = "false"
    "SCM_DO_BUILD_DURING_DEPLOYMENT"      = "true"
    "WEBSITE_RUN_FROM_PACKAGE"            = "1"
  }
}
