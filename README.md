<h1>Project Documentation</h1>

<h2>Overview</h2>
      <p>This project is designed to provide a streamlined interface for searching and displaying ferry routes. It leverages Django for the backend, including form handling, API integrations with various suppliers, and dynamic data rendering in the frontend using templates.</p>


<h2 id="structure">1. Project Structure</h2>
        <pre>
appname/
|-- ferri_routes/
|   |-- static/
|   |   |-- styles.css
|   |-- templates/
|   |   |-- index.html
|   |-- __init__.py
|   |-- admin.py
|   |-- apps.py
|   |-- forms.py
|   |-- models.py
|   |-- services.py
|   |-- tests.py
|   |-- urls.py
|   |-- views.py
|-- .env
|-- manage.py
        </pre>

<h2 id="installation">2. Installation and Setup</h2>
        <p>To set up the project locally, follow these steps:</p>
        <ol>
            <li>Clone the repository:
                <pre>
git clone https://github.com/medinamaria90/FerrySearching.git projectname
cd projectname
                </pre>
</li>
<li>Create and activate a virtual environment:
    <pre>
python3 -m venv env
source env/bin/activate  
# On Windows use env\Scripts\activate
    </pre>
</li>
<li>Install dependencies:
    <pre>
pip install -r requirements.txt
    </pre>
</li>
</li>
<li>Run the app and access it at <code>localhost</code>.
<pre>
python manage.py runserver
    </pre>
</li>
</ol>

<h2 id="environment">3. Environment Configuration</h2>
        <p>Sensitive information such as API tokens and user and password are stored in the <code>.env</code> file. This file shouldn't be committed to version control, but I've commited it so you can access it easily.
        </p>
        <pre>
SUPPLIER_1_TOKEN=your_supplier_1_token
SUPPLIER_2_USERNAME=your_supplier_2_username
SUPPLIER_2_PASSWORD=your_supplier_2_password
        </pre>

<h2 id="flow">4. Application Flow</h2>
        <ol>
            <li>The user accesses the main page and fills out the ferry search form.</li>
            <li>The form data is submitted and handled by the <code>index</code> view in <code>views.py</code>.</li>
            <li>The <code>SupplierManager</code> class in <code>services.py</code> fetches and normalizes data from different suppliers.</li>
            <li>The results are rendered back in the <code>index.html</code> template.</li>
        </ol>

<h2 id="code">5. Code Explanation</h2>

<h3 id="services">services.py</h3>
      <p>This file contains classes that handle API interactions with ferry suppliers. It follows an abstract base class pattern to ensure scalability and uniformity.</p>
      <ul>
          <li><code>BaseSupplier</code>: Abstract base class defining the structure for all supplier classes.</li>
          <li><code>Supplier1</code> and <code>Supplier2</code>: Implementations of <code>BaseSupplier</code> for specific suppliers. Each has methods to fetch and normalize data.</li>
          <li><code>SupplierManager</code>: Manages multiple suppliers and consolidates data for rendering.</li>
      </ul>

<h3 id="views">views.py</h3>
      <p>Handles HTTP requests and responses.</p>
        <ul>
            <li><code>index</code>: Manages the search form, calls the <code>SupplierManager</code> to fetch data, and renders the results.</li>
        </ul>

<h3 id="forms">forms.py</h3>
        <p>Defines the form used to search for ferry routes.</p>
        <ul>
            <li><code>SearcherForm</code>: A Django form that includes fields for route, departure date, and optional return date.</li>
        </ul>
        
  <h3 id="urls">urls.py</h3>
        <p>Defines URL patterns for the application.</p>
        <ul>
            <li>Maps the root URL to the <code>index</code> view.</li>
        </ul>
        
  <h3 id="index">index.html</h3>
        <p>The main template for rendering the search form and displaying results.</p>
        <ul>
            <li>Uses Bootstrap for styling and layout.</li>
            <li>Includes JavaScript for client-side validation.</li>
        </ul>
        
<h2 id="code">6. Images</h2>

![image](https://github.com/medinamaria90/FerrySearching/assets/131414823/618c136c-d58f-4e57-af47-26a18179e6fa)

![image](https://github.com/medinamaria90/FerrySearching/assets/131414823/b61fc22b-466c-4916-9e1a-ef0a3b34c4f7)

<br>

<p>Thank you!</p>
<a href="www.mmcprojects.dev">Go to my portfolio to see more projects<a>

  
  
    

