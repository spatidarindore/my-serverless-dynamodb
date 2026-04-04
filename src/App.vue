<template>
  <div>
    <h1>User Registration</h1>
    <form @submit.prevent="submitForm">
      <input v-model="name" placeholder="Enter name" required />
      <input v-model="email" placeholder="Enter email" required />
      <button type="submit">Submit</button>
    </form>
    <p>{{ message }}</p>

    <h2>Registered Users</h2>
    <ul>
      <li v-for="user in users" :key="user.id">
        <strong>{{ user.name }}</strong> — {{ user.email }}
      </li>
    </ul>
  </div>
</template>

<script>
export default {
  data() {
    return {
      name: '',
      email: '',
      message: '',
      users: []   // store fetched users
    }
  },
  methods: {
    async submitForm() {
      try {
        const response = await fetch('https://zen4z8f70l.execute-api.ap-south-1.amazonaws.com/dev/items', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ name: this.name, email: this.email })
        })
        const data = await response.json()
        this.message = data.message

        // refresh user list after adding new one
        this.fetchUsers()
      } catch (err) {
        this.message = 'Error: ' + err.message
      }
    },
    async fetchUsers() {
      try {
        const response = await fetch('https://zen4z8f70l.execute-api.ap-south-1.amazonaws.com/dev/items')
        const data = await response.json()
        this.users = data.items || []   // assuming API returns { items: [...] }
      } catch (err) {
        console.error('Error fetching users:', err)
      }
    }
  },
  mounted() {
    // load users when component mounts
    this.fetchUsers()
  }
}
</script>