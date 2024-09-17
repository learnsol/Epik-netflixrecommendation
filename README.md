A Netflix recommendation RAG Chat bot ( Part of Raghack 2024)

Needs the following resources 
  1. Azure OpenAI resource - A base model, i have used gpt-4o-mini
  2. Azure AI Search - to index and leverage AI ML to create vectors using HSNW Algorithm and use semantic search
  3. Azure Storage account - Blob storage holds the source document as a pdf
  4. Azure Service Managed Identities - Ensure all services can talk to each other leveraging inbuild RBAC Roles without the need to store credentials any where

![image](https://github.com/user-attachments/assets/1003f9a8-44ec-4c9f-94fa-57c441d24ef0)
