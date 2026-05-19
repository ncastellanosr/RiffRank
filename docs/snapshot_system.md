# Snapshot System
*April 25, 2026. 3:00 p.m.*
The raw data storage has to be convenient. The raw payloads are stored as JSON files, and both the folder structure and naming convention for files and folders have to be well defined. A snapshot system was proposed before, where each snapshot was an individual consumable data unit. However, that makes idempotency hard. If the ingestion was to be executed twice using the same artist_ids.txt file, then two different snapshots generated on two different times will have the exact same content. So perhaps, one doesn't need multiple snapshots, unless the API response format changed. Or better, the snapshots should not be differentiated by the execution instance or generation time, rather by version. This means that the same consumable data unit will be generated and mantained accross multiple executions. The following folder structure and naming conventions should suffice to mantain and escalate such a system.

![[Snapshot Diagram.png]]
