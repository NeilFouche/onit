# Django Backend

## Documentation
* [Settings](https://docs.djangoproject.com/en/5.1/topics/settings/)
* [List of Settings](https://docs.djangoproject.com/en/5.1/ref/settings/)
* [Deployment Checklist](https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/)
* [Database settings](https://docs.djangoproject.com/en/5.1/ref/settings/#databases)
* [Password Validation](https://docs.djangoproject.com/en/5.1/topics/auth/passwords/#password-validation)
* [Internationalization](https://docs.djangoproject.com/en/5.1/topics/i18n/)
* [Static files](https://docs.djangoproject.com/en/5.1/howto/static-files/)
* [Default Primary Key](https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field)

## File structure
#### `onitweb`
This directory houses project-level configuration and entry-point files

 - `settings.py`: If this file grows large, consider splitting it into modular settings files (e.g., settings/base.py, settings/development.py, settings/production.py) for better management of environments.

#### `.env`
A place to store sensitive settings (e.g., database credentials) and using a library like django-environ can further enhance security.

#### `api` App
Serves as the main application for your website’s frontend functionality.

#### `services`
This is to serve as a domain-specific logic hub for the backend.

#### `utils`
This is to serve as a domain-specific logic hub for the backend.

! Command to create requirements.txt:
```bash
pipenv requirements > requirements.txt
```

! Tools to use for external migrations:
- Alembic: For schema migrations or Python scripts for bulk data migrations.

## Amazon RDS Database

### Database details
**Instance ID:** onit-id\
**Database Name:** onitdb\
**Engine version:** MySQL 8.0.39\
**Maintenance window:** Saturdays 21:00-21:30\
**Backup window:** Daily 20:00-20:30

#### Technical specifications:
**Class:** db.t4g.micro\
**Virtual CPUs:** 2\
**RAM:** 1 GB

### Storage
**Encrytion:** Enabled\
**Storage type:** General Purpose SSD (gp3)\
**Storage capacity:** 20 GiB (20 x 2^30 bytes)\
**Provisioned I/O  (IOPS):** 3000\
**Storage throughput:** 125 MiBps (125 x 2^20 bits per second)\
**Autoscaling:** Disabled

### Caching
**Cache:** Redis (serverless)
**Name:** onit-db-redis-cachecluster
**Engine version:** 7.1
**Encryption in transit:** Enabled
**Maximum data storage:** 1 GB
**Maximum request rate:** 1000 ECPUs per second
**Automatic backups:** Enabled
**Backup window:** Daily 20:00
**Backup retention:** 1 day

### Logging
* Error logs

### Notes

* Consider creating a Blue/Green Deployment to minimize downtime during upgrades
You may want to consider using Amazon RDS Blue/Green Deployments and minimize your downtime during upgrades. A Blue/Green Deployment provides a staging environment for changes to production databases. RDS User Guide  Aurora User Guide

* Easy path homogeneous data migrations from EC2 database to RDS
With integrated homogenous data migration powered by AWS DMS, the Amazon RDS console leverages simple and performant data migration from EC2 database to equivalent RDS database. To get started, select an existing RDS database and choose the Migrate data from EC2 database in the Actions menu. Make sure you check the supported engine types and feature limitations. Learn more

* Introducing Global Database writer endpoint
Each global cluster now has a writer endpoint that you can use to send your application's requests to the writer instance in the primary cluster of your Global Database. Aurora automatically updates the endpoint upon a cross-region failover or switchover operation, ensuring that requests are routed to the writer instance in the new primary cluster without the need for changes to your application code or configuration. Learn more

* Introducing Global Database writer endpoint
Each global cluster now has a writer endpoint that you can use to send your application's requests to the writer instance in the primary cluster of your Global Database. Aurora automatically updates the endpoint upon a cross-region failover or switchover operation, ensuring that requests are routed to the writer instance in the new primary cluster without the need for changes to your application code or configuration. Learn more

* Introducing Aurora I/O-Optimized
Aurora’s I/O-Optimized is a new cluster storage configuration that offers predictable pricing for all applications and improved price-performance, with up to 40% costs savings for I/O-intensive applications.

* New monitoring view is available
RDS now supports a new monitoring view which includes Performance Insights and CloudWatch metrics. To access the new monitoring view, select Modify to modify your database and turn on Performance Insights.

### Database metrics

The following metrics indicate how well the database instance is handling the requests.

#### CPUUtilization (%):

**Why it's important**: High CPU utilization (typically above 80-90% for extended periods) indicates that the instance is using most or all of its CPU capacity. This suggests that the instance might be under heavy load, possibly causing slower performance.

**When it's a concern**: If CPU utilization remains high, it may lead to degraded performance, and it might be time to scale up (move to a larger instance) or optimize your queries and application.

#### DiskQueueDepth (Count):

**Why it's important**: If there is a high number of requests queued for disk I/O (DiskQueueDepth), it indicates disk performance bottlenecks. This can happen when the database is trying to perform read/write operations faster than the disk can handle, which can slow down database performance.

**When it's a concern**: A high value over time (e.g., more than 2 or 3) suggests the disk is not keeping up with I/O requests, and the instance may struggle to handle more traffic.

#### Read/WriteLatency (ms):

**Why it's important**: High latency in read and write operations shows that the database is taking longer to fetch or store data, which may indicate resource exhaustion or inefficient queries.

**When it's a concern**: Latencies above a few milliseconds can start to affect user experience, and consistently high latencies could point to database strain.

#### FreeableMemory (Bytes):

**Why it's important**: If the instance runs low on memory, it might start swapping to disk, which significantly impacts performance. Freeable memory dropping too low could indicate the need for more memory.

**When it's a concern**: If free memory is consistently low, the database might be under heavy load, and performance could degrade.

#### SwapUsage (Bytes):

**Why it's important**: If the system is using swap space, it indicates that the physical RAM is exhausted, and the system is swapping data to disk, which can severely degrade performance.

**When it's a concern**: If swap usage is increasing, it’s a clear sign the instance doesn't have enough memory to handle the workload efficiently.

#### TotalIOPS (Count/s):

**Why it's important**: This metric shows the overall I/O load on the instance. If your total IOPS is very high, it could indicate that the database is handling many I/O requests, possibly stressing the storage system.

**When it's a concern**: If IOPS are consistently high and the instance performance begins to degrade, consider scaling the instance or optimizing the queries to reduce I/O operations.

#### Network Throughput (NetworkReceiveThroughput/NetworkTransmitThroughput):

**Why it's important**: If your network throughput is maxed out, it could suggest that your instance is struggling to send or receive data, which could impact performance, especially if you have a lot of incoming/outgoing traffic.

**When it's a concern**: Network throughput becoming a bottleneck might indicate a need for a larger instance with better networking capabilities or optimizing the data transfer.