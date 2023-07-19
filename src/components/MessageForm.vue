<template>
  <h1>Message</h1>
  <div>
    <select v-model="selectedPlatform">
      <option v-for="platform in platforms" :key="platform" :value="platform">
        {{ platform }}
      </option>
    </select>

    <select v-model="selectedSender">
      <option
        v-for="sender in filterSendersByPlatforms"
        :key="sender"
        :value="sender"
      >
        {{ sender }}
      </option>
    </select>
  </div>
  <div>
    <input type="text" :value="receiverURL" placeholder="ReceiverURL" />
  </div>
  <div>
    <h3>Message</h3>
    <div>
      <select v-model="selectedTemplate">
        <option v-for="template in templates" :key="template" :value="template">
          {{ template }}
        </option>
      </select>

      <button @click="createAndEditTemplate">Create and Edit Template</button>
    </div>
    <div>
      <textarea v-model="message" placeholder="Message"></textarea>
    </div>
  </div>

  <h4>Target Settings</h4>
  <div class="checkbox-message">
    <label>
      <input type="checkbox" v-model="targetSettings.changedPosition" />{{
        targetSettingsMessages.changedPosition
      }}
    </label>
    <label>
      <input type="checkbox" v-model="targetSettings.alreadyConnected" />{{
        targetSettingsMessages.alreadyConnected
      }}
    </label>
    <label>
      <input type="checkbox" v-model="targetSettings.followCandidate" />{{
        targetSettingsMessages.followCandidate
      }}
    </label>
  </div>
</template>

<script lang="ts">
import { ref } from "vue";

export default {
  data() {
    return {
      platforms: ["Linkedin", "Facebook", "Zalo"],
      senders: {
        Linkedin: ["Nguyen Van A", "Nguyen Van D"],
        Facebook: ["Nguyen Van B"],
        Zalo: ["Nguyen Van C"],
      } as Record<string, string[]>,
      templates: ["template1", "template2"],
      selectedPlatform: "",
      selectedSender: "",
      receiverURL: "",
      selectedTemplate: "",
      message: "",
      targetSettings: {
        changedPosition: false,
        alreadyConnected: false,
        followCandidate: false,
      },
      targetSettingsMessages: {
        changedPosition:
          "Do not send message if current company or position is changed",
        alreadyConnected: "Do not send to people you've already connected with",
        followCandidate: "Follow candidate when sending invite message",
      },
    };
  },
  computed: {
    filterSendersByPlatforms() {
      return this.senders[this.selectedPlatform] || [];
    },
  },
  methods: {
    createAndEditTemplate() {},
  },
};
</script>

<style>
.checkbox-message {
  display: flex;
  flex-direction: column;
}
</style>
