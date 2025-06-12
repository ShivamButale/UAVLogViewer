<template>
  <div class="chat-box">
    <input
      v-model="userQuery"
      @keyup.enter="sendQuery"
      type="text"
      placeholder="Ask a question about the log"
      class="chat-input"
    />
    <div v-if="response" class="chat-response">
      {{ response }}
    </div>
  </div>
</template>

<script>
export default {
    name: 'ChatBox',
    props: {
        sessionId: {
            type: String,
            required: true
        }
    },
    data () {
        return {
            userQuery: '',
            response: ''
        }
    },
    methods: {
        async sendQuery () {
            if (!this.userQuery.trim()) {
                return
            }

            try {
                const res = await fetch('http://localhost:8000/chat', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({
                        sessionId: this.sessionId,
                        userQuery: this.userQuery
                    })
                })

                const data = await res.json()
                this.response = data.response || 'No response from model'
                this.userQuery = ''
            } catch (err) {
                this.response = 'Error fetching response from backend'
                console.error(err)
            }
        }
    }
}
</script>

<style scoped>
.chat-box {
  position: fixed;
  bottom: 20px;
  left: 20px;
  right: 20px;
  background: #f9f9f9;
  padding: 10px;
  border-top: 1px solid #ddd;
  box-shadow: 0 -1px 5px rgba(0, 0, 0, 0.1);
  z-index: 1000;
}

.chat-input {
  width: 100%;
  padding: 10px;
  font-size: 16px;
  border: 1px solid #ccc;
  border-radius: 6px;
  outline: none;
}

.chat-response {
  margin-top: 10px;
  background: #e6f7ff;
  padding: 10px;
  border-radius: 4px;
}
</style>
