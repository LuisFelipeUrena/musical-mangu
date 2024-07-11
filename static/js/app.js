new Vue({
    el: '#app',
    template: `
        <div>
            <h1>Data Warehouse Explorer</h1>
            <div v-if="loading">Loading...</div>
            <div v-else>
                <div v-for="(tables, schema) in schemaInfo" :key="schema">
                    <h2>{{ schema }}</h2>
                    <ul>
                        <li v-for="(columns, table) in tables" :key="table">
                            {{ table }}
                            <button @click="getDescription(schema, table)">Get Description</button>
                            <p v-if="descriptions[schema + '.' + table]">
                                {{ descriptions[schema + '.' + table] }}
                            </p>
                        </li>
                    </ul>
                </div>
            </div>
        </div>
    `,
    data: {
        schemaInfo: {},
        descriptions: {},
        loading: true
    },
    mounted() {
        this.getSchema();
    },
    methods: {
        getSchema() {
            this.loading = true;
            axios.get('/api/schema')
                .then(response => {
                    this.schemaInfo = response.data;
                    this.loading = false;
                })
                .catch(error => {
                    console.error("Error fetching schema:", error);
                    this.loading = false;
                });
        },
        getDescription(schema, table) {
            axios.get(`/api/description/${schema}/${table}`)
                .then(response => {
                    this.$set(this.descriptions, schema + '.' + table, response.data.description);
                })
                .catch(error => {
                    console.error("Error fetching description:", error);
                });
        }
    }
});