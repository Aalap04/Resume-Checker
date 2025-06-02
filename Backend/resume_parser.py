import re

def extract_skills(text):
    # Example tech keywords; expand this list
    keywords = ['python', 'java', 'aws', 'docker', 'streamlit', 'sql',  'python', 'java', 'javascript', 'typescript', 'c++', 'c#', 'php', 'ruby', 'go', 'rust',
        'swift', 'kotlin', 'scala', 'perl', 'r', 'matlab', 'julia', 'dart', 'elixir', 'erlang',
        'haskell', 'clojure', 'f#', 'lua', 'groovy', 'pascal', 'fortran', 'cobol', 'assembly',
        'vb.net', 'visual basic', 'objective-c', 'solidity', 'verilog', 'vhdl', 'bash', 'shell',
        'powershell', 'batch', 'awk', 'sed', 'html', 'css', 'sass', 'scss', 'less', 'bootstrap', 'tailwind', 'bulma', 'foundation',
        'react', 'angular', 'vue', 'svelte', 'ember', 'backbone', 'jquery', 'next.js', 'nuxt.js',
        'gatsby', 'express', 'fastify', 'koa', 'nest.js', 'django', 'flask', 'fastapi', 'tornado',
        'spring', 'spring boot', 'struts', 'hibernate', 'rails', 'sinatra', 'laravel', 'symfony',
        'codeigniter', 'asp.net', 'mvc', 'web api', 'blazor', 'phoenix', 'gin', 'echo', 'fiber', 'mysql', 'postgresql', 'sqlite', 'oracle', 'sql server', 'mongodb', 'cassandra', 'redis',
        'elasticsearch', 'solr', 'neo4j', 'dynamodb', 'firebase', 'couchdb', 'mariadb', 'influxdb',
        'timescaledb', 'cockroachdb', 'fauna', 'supabase', 'planetscale', 'arangodb', 'orientdb',
        'amazon rds', 'azure sql', 'google cloud sql', 'snowflake', 'bigquery', 'redshift',
        'databricks', 'clickhouse', 'apache drill', 'presto', 'apache spark', 'hadoop', 'aws', 'azure', 'gcp', 'google cloud', 'digital ocean', 'linode', 'vultr', 'heroku',
        'vercel', 'netlify', 'cloudflare', 'fastly', 'aws lambda', 'azure functions', 
        'google cloud functions', 'aws ec2', 'aws s3', 'aws rds', 'aws dynamodb', 'aws sqs',
        'aws sns', 'aws cloudformation', 'aws cloudwatch', 'azure devops', 'azure ad',
        'google kubernetes engine', 'amazon eks', 'azure kubernetes service', 'cloud run',
        'app engine', 'compute engine', 'elastic beanstalk', 'lightsail', 'fargate', 'jenkins', 'gitlab ci', 'github actions', 'circleci', 'travis ci',
        'ansible', 'terraform', 'vagrant', 'chef', 'puppet', 'salt', 'helm', 'istio', 'consul',
        'vault', 'nomad', 'prometheus', 'grafana', 'elk stack', 'splunk', 'datadog', 'new relic',
        'nagios', 'zabbix', 'pagerduty', 'apache', 'nginx', 'haproxy', 'traefik', 'envoy',
        'cloudformation', 'arm templates', 'pulumi', 'cdk', 'serverless framework',  'pandas', 'numpy', 'scikit-learn', 'tensorflow', 'pytorch', 'keras', 'opencv', 'nltk',
        'spacy', 'gensim', 'matplotlib', 'seaborn', 'plotly', 'bokeh', 'tableau', 'power bi',
        'qlik', 'looker', 'jupyter', 'anaconda', 'r studio', 'apache spark', 'apache kafka',
        'apache airflow', 'luigi', 'dask', 'ray', 'mlflow', 'kubeflow', 'sagemaker', 'azure ml',
        'google ai platform', 'vertex ai', 'hugging face', 'transformers', 'bert', 'gpt',
        'stable diffusion', 'langchain', 'llamaindex', 'vector databases', 'pinecone', 'weaviate', 'android', 'ios', 'react native', 'flutter', 'xamarin', 'ionic', 'cordova', 'phonegap',
        'swift ui', 'jetpack compose', 'kotlin multiplatform', 'unity', 'unreal engine',
        'firebase', 'realm', 'core data', 'room', 'sqlite', 'push notifications', 'in-app purchases']
    text = text.lower()
    found = [kw for kw in keywords if kw in text]
    return list(set(found))
