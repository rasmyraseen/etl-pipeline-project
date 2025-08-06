## Architectural Decisions & Technical Trade-offs (section 01)

### 1. **Choice of Spark for ETL**

* **Why Spark?**
  PySpark is chosen for the ETL pipeline because of its ability to handle large datasets efficiently. It provides both parallel processing and fault tolerance. Additionally, Spark integrates seamlessly with various data sources, including SQL databases and file formats (CSV, Parquet, etc.), making it an ideal choice for scalable ETL tasks.

* **Trade-off:**

  * **Learning Curve:** PySpark has a steeper learning curve compared to simpler libraries like Pandas or traditional Python-based ETL libraries. However, the scalability benefit outweighs this, especially when dealing with large data volumes.
  * **Setup Complexity:** Setting up Spark, especially inside Docker containers, is more complex compared to using lightweight frameworks. However, once set up, Spark provides significant performance gains for large datasets.

### 2. **Docker Containerization**

* **Why Docker?**
  Docker was used to containerize the entire ETL pipeline, ensuring that the project environment is consistent across development, testing, and production. Docker also simplifies dependency management and avoids conflicts between local environments.

* **Trade-off:**

  * **Overhead:** Containerization introduces some overhead, particularly when running Spark in local mode. This could impact performance when compared to running Spark on a dedicated cluster.
  * **Networking Complexity:** Docker's networking model can sometimes add complexity when connecting containers to external services, like the SQL Server database. However, using `host.docker.internal` resolves the networking issue in most cases.

### 3. **SQL Server for Data Storage**

* **Why SQL Server?**
  SQL Server was selected as the target storage for the enriched data due to its familiarity and compatibility with the organization's existing data infrastructure. SQL Server also supports ACID properties, ensuring the integrity of the data during ETL operations.

* **Trade-off:**

  * **SQL Server Limitations:** While SQL Server is a reliable RDBMS, it may not scale as well as other distributed databases like Hadoop or NoSQL databases. However, SQL Server's familiarity, robust support, and integration with existing tools make it suitable for the project.
  * **Integration Complexity:** The integration of PySpark with SQL Server requires using the JDBC driver. This adds complexity to the code and requires managing additional dependencies (e.g., `mssql-jdbc`).

### 4. **API Integration for Currency Conversion**

* **Why API Integration?**
  An external exchange rate API was integrated to convert sales data into USD. This allows the ETL pipeline to fetch real-time currency rates, ensuring that the data is accurate and up-to-date.

* **Trade-off:**

  * **External Dependency:** Relying on an external API adds a dependency outside the control of the organization. This introduces potential failure points (e.g., API downtime or rate-limiting).
  * **API Rate Limiting:** The external API may have rate limits, which could cause delays if the ETL process is executed at a high frequency. This was mitigated by implementing error handling and fallback mechanisms.

### 5. **Data Validation & Error Handling**

* **Why Rigorous Data Validation?**
  Data validation ensures that the data is cleaned and consistent before further processing or storage. This includes handling null values, duplicates, and ensuring that the data matches expected formats.

* **Trade-off:**

  * **Processing Overhead:** Implementing detailed validation checks adds overhead to the ETL process. However, it ensures that only high-quality data is inserted into the target database, preventing errors and ensuring data integrity.
  * **Complexity:** The logic for handling rejected records, logging, and fallbacks can increase the complexity of the code, but it is necessary for a robust and fault-tolerant pipeline.

### 6. **Error Handling and Logging**

* **Why Robust Error Handling?**
  Error handling ensures that the pipeline can fail gracefully and provide useful insights when something goes wrong. Logging provides traceability and allows the team to identify and fix issues efficiently.

* **Trade-off:**

  * **Performance Impact:** Extensive logging and error handling might impact performance. However, it is a necessary trade-off for production-grade systems to ensure maintainability and troubleshooting.
  * **Code Complexity:** The logic for logging errors and archiving rejected records adds complexity. Yet, it's crucial for ensuring data consistency and troubleshooting issues in production.

### 7. **Data Processing in Local Mode**

* **Why Local Mode?**
  Spark was configured in local mode for development and testing purposes. It allows for quicker iterations during development without the overhead of setting up a cluster.

* **Trade-off:**

  * **Limited Scalability:** Running Spark in local mode limits scalability and doesn’t utilize the distributed power of Spark. In production, Spark would ideally run on a cluster or cloud infrastructure, but local mode is sufficient for small-scale testing.
  * **Single Machine Limitation:** Local mode processes data on a single machine, which could lead to performance issues with larger datasets. In production, this would be scaled out to a cluster for better performance.

### 8. **Jupyter Notebook for ETL Development**

* **Why Jupyter Notebook?**
  Jupyter was chosen as the interface for developing and testing the ETL pipeline. It allows for easy interaction with the data, quick iterations, and visual feedback, which is ideal during the development phase.

* **Trade-off:**

  * **Limited Production Usage:** Jupyter is great for development but not typically used for production. For large-scale production, scripts run via `spark-submit` would be more appropriate. However, for prototyping and testing, Jupyter is a perfect tool.

### 9. GitHub for Version Control and Collaboration
* **Why GitHub?**
GitHub was chosen for version control and collaboration, providing a platform for team members to work together efficiently. It enables seamless tracking of code changes, reviewing pull requests, and managing issues. GitHub ensures the codebase is always synchronized across different environments, making collaboration easier and more organized.

* **Trade-off:**

Learning Curve for New Users: While GitHub offers powerful features for version control, there is a learning curve for new users, especially those unfamiliar with Git or branching strategies. However, the benefits of collaboration, code tracking, and CI/CD automation outweigh the initial challenges.

### 10. GitHub Actions for CI/CD
* **Why GitHub Actions?**
GitHub Actions was integrated to automate the CI/CD pipeline, ensuring that every change to the repository is automatically built, tested, and deployed. It streamlines the process of validating changes, making it easier to catch errors early and ensuring that code is always production-ready.

* **Trade-off:**

Complex Setup: Setting up GitHub Actions for CI/CD requires an understanding of workflows and YAML configuration, which may introduce complexity. However, once set up, it provides a powerful automation tool that greatly reduces manual intervention, speeds up the development process, and ensures code quality.

### Final Thoughts

Each technical decision made in this project was driven by the need to balance performance, maintainability, scalability, and simplicity.The most significant trade-off was managing the complexity of Docker and Spark configurations in exchange for environment consistency and scalability. Despite the initial setup effort, Docker and PySpark offered a dependable and portable environment for building and testing the ETL pipeline.Incorporating Jupyter Notebook allowed for rapid prototyping and interactive data processing during development. GitHub ensured robust version control and team collaboration, while GitHub Actions introduced a lightweight CI/CD layer to automate testing and build validation.

Going forward, the system could be enhanced by:

* **Scaling for larger datasets using cloud-based Spark clusters (e.g., AWS EMR, Azure Synapse).**

* **Strengthening fault tolerance and error recovery.**

* **Expanding CI/CD pipelines to include automated testing and deployment workflows.**

These improvements would further align the project with production-grade data engineering standards.