# kong-ai-plugin-guru

## Demo

URL: www.placeholder.com.br

## About

This repository contains an Addon to the Kong Developer Portal that leverages ChatGPT to create Kong plugins. The goal is to help new developers create new plugins more easily and quickly.

## The improvement

![normalway-versus-aipluginguruway](images/normalway-versus-aipluginguruway.png)

### The Normal Way:
A new developer has to go through at least these four steps:

1) **Choose a plugin:** The developer needs to select a plugin that solves its problems. Sometimes, it's not clear which plugin to use because they have different names. For example, OpenID Connect (for authentication and authorization) and OpenTelemetry (for tracing).

2) **Understand the basic structure:** Each plugin has its own basic structure described in its documentation.

3) **Company-Specific Configurations:** Most plugins require company-specific configurations, such as endpoints, client IDs, client secrets, and other settings. The new developer has to review the code of the already installed plugins or seek assistance from others to understand these specifications.

4) **My API-Specific Configurations:** The new developer has to modify the basic use of the plugins to include specific configurations for their own API."

### The AI Plugin Guru Way:

1) **Write what you need:** Write in natural language (any language: english, portugues, spanish...) what you need the plugin to do, and ChatGPT will consult the configurations of the plugins already installed in your company and provide you with the declarative Kong configuration of the plugin you need. And that's it.


## Examples

### User: I need to add authentication and authorization to my api "accounts". Kong needs to check if the token has the role "admin" to acess my api.

This plugin is already configured in my company, and AI Plugin Guru is going to use this configuration as a base to suggest a new one:

```
  - name: openid-connect
    instance_name: example-openid-connect
    enabled: true
    config:
        auth_methods:
        - bearer
        introspect_jwt_tokens: false
        verify_signature: false
        client_id: 
        - "{vault://aws/open-id-connect/client_id}"
        client_secret: 
        - "{vault://aws/open-id-connect/client_secret}"
        verify_claims: true
        issuer: http://keycloak.opus-software.com.br:9000/auth/realms/master/.well-known/openid-configuration
        roles_claim:
        - resource_access
        - api-teste
        - roles
        roles_required:
        - admin
```

Plugin created by Ai Plugin Guru:

![openidconnet](images/openidconnet.png)



### User: I need to add tracing to my api "clients".

This plugin is already configured in my company, and AI Plugin Guru is going to use this configuration as a base to suggest a new one:
```
plugins:
- name: opentelemetry
instance_name: example-opentemetry
config:
    endpoint: "http://opentelemetry-collector-opus-software.otl:4318/v1/traces"
```
Plugin created by Ai Plugin Guru:

![opentelemetry](images/opentelemetry.png)



## How it works

## Flow

![Screenshot](images/flow.png)

### 1. Get a developer key from the Developer Portal API.

### 2. Get the json list of plugins already installed.

### 3. Get the response from ChatGPT.

## Build

Install Kong:
```
helm --namespace kong install kong kong/kong  --values ./kong/embedded.yaml --create-namespace
```

Add the services, routes and plugins:
```
deck sync --workspace default --select-tag ai-plugin-guru --state ./deck/ai-plugin-guru.yaml
```

Add examples plugins:
```
deck sync --workspace default --select-tag example-plugins --state ./deck/example-plugins.yaml
```

Add the Ai Plugin Guru to the Devportal:
```
/portal.conf.yaml: Add the lines in ./developer-portal/portal.conf.yaml
/content: Add the file ./developer-portal/content/ai-plugin-guru.txt
/themes/base/layouts: Add the file ./developer-portal/themes/base/layouts/ai-plugin-guru.html
```