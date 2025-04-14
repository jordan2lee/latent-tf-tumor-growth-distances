# Troubleshooting

# Timeout During Entrez ID Conversion

Running `bash scripts/process.sh <CANCER> <DIR>` results in timeout issues. Due to internet bandwidth, simply rerun command. 

*Error message:*
```bash
Error in curl::curl_fetch_memory(url, handle = handle) : 
  Timeout was reached: [www.ensembl.org:443] Operation timed out after ... milliseconds with ... bytes received
Calls: useDataset ... request_fetch -> request_fetch.write_memory -> <Anonymous>
```
