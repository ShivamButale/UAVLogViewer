<template>
  <div id="app" style="height: 100%;">
    <router-view />

    <!-- 💬 Show ChatBox only when sessionId is set -->
    <ChatBox v-if="sessionId" :sessionId="sessionId" />
  </div>
</template>

<script>
import ChatBox from './components/ChatBox.vue'

export default {
    name: 'App',
    components: {
        ChatBox
    },
    data () {
        return {
            sessionId: '' // Start empty, set dynamically
        }
    },
    created () {
        // Listen for the emitted session ID from uploader
        this.$root.$on('session-id-updated', (newSessionId) => {
            this.sessionId = newSessionId
            console.log('🔗 Session ID received in App.vue:', newSessionId)
        })
    }
}
</script>

<style>
@import url('https://fonts.googleapis.com/css?family=Nunito+Sans&display=swap');

#app {
  font-family: 'Nunito Sans', sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}

html,
body {
  overscroll-behavior-y: contain;
}
</style>
