<template>
  <div>
    <h1>Message</h1>
    <div class="select-platform-and-sender">
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
    <div class="receiver-url">
      <input type="text" :value="receiverURL" placeholder="ReceiverURL" />
    </div>
    <div class="message">
      <h3>Message</h3>
      <div class="select-template">
        <select v-model="selectedTemplate">
          <option
            v-for="template in templates"
            :key="template"
            :value="template"
          >
            {{ template }}
          </option>
        </select>

        <button @click="createAndEditTemplate">Create and Edit Template</button>
      </div>
      <div class="message-box">
        <textarea v-model="message" placeholder="Message"></textarea>
      </div>
    </div>

    <h4>Target Settings</h4>
    <div class="checkbox-message">
      <label>
        <input type="checkbox" v-model="targetSettings.changedPosition" />
        {{ targetSettingsMessages.changedPosition }}
      </label>
      <label>
        <input type="checkbox" v-model="targetSettings.alreadyConnected" />
        {{ targetSettingsMessages.alreadyConnected }}
      </label>
      <label>
        <input type="checkbox" v-model="targetSettings.followCandidate" />
        {{ targetSettingsMessages.followCandidate }}
      </label>
    </div>

    <button @click="preview">Preview and Send</button>

    <div v-if="showPreviewModel" class="model">
      <div class="model-content">
        <span class="close" @click="closeModel">&times;</span>
        <h3>Preview</h3>
        <p>{{ previewData }}</p>
        <button @click="send">Send</button>
      </div>
    </div>
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
      showPreviewModel: false,
      previewData: "",
    };
  },
  computed: {
    filterSendersByPlatforms() {
      return this.senders[this.selectedPlatform] || [];
    },
  },
  methods: {
    createAndEditTemplate() {},
    preview() {
      const previewModel = {
        platform: this.selectedPlatform,
        sender: this.selectedSender,
        receiverURL: this.receiverURL,
        template: this.selectedTemplate,
        message: this.message,
        targetSettings: this.targetSettings,
      };
      this.previewData = JSON.stringify(previewModel);
      this.showPreviewModel = true;
    },
    closeModel() {
      this.showPreviewModel = false;
    },
    send() {
      const sendMessage = {
        platform: this.selectedPlatform,
        sender: this.selectedSender,
        receiverURL: this.receiverURL,
        template: this.selectedTemplate,
        message: this.message,
        targetSettings: this.targetSettings,
      };
      this.selectedPlatform = "";
      this.selectedSender = "";
      this.receiverURL = "";
      this.selectedTemplate = "";
      this.message = "";
      this.targetSettings.alreadyConnected = false;
      this.targetSettings.changedPosition = false;
      this.targetSettings.followCandidate = false;
    },
  },
};
</script>

<style>
.checkbox-message {
  display: flex;
  flex-direction: column;
}
</style>
