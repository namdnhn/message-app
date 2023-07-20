<template>
  <div class="custom-background">
    <h1>Message</h1>
    <div class="select-platform-and-sender">
      <label>Select platform: </label>
      <select class="custom-select" v-model="selectedPlatform">
        <option v-for="platform in platforms" :key="platform" :value="platform">
          {{ platform }}
        </option>
      </select>

      <label> Select User: </label>
      <select class="custom-select" v-model="selectedSender">
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
      <label>Receiver URL: </label>
      <input
        class="custom-textbox"
        type="text"
        :value="receiverURL"
        placeholder="ReceiverURL"
      />
    </div>
    <div class="message">
      <h3>Message</h3>
      <div class="select-template">
        <select class="custom-select" v-model="selectedTemplate">
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
        <textarea
          class="custom-textbox"
          v-model="message"
          placeholder="Message"
        ></textarea>
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
import { computed, reactive, ref } from "vue";

export default {
  setup() {
    const platforms = ref(["Linkedin", "Facebook", "Zalo"]);
    const selectedPlatform = ref("");

    const senders = reactive<Record<string, string[]>>({
      Linkedin: ["Nguyen Van A", "Nguyen Van D"],
      Facebook: ["Nguyen Van B"],
      Zalo: ["Nguyen Van C"],
    });
    const selectedSender = ref("");
    const filterSendersByPlatforms = computed(() => {
      return senders[selectedPlatform.value] || [];
    });

    const templates = ref(["template1", "template2"]);
    const selectedTemplate = ref("");
    const createAndEditTemplate = () => {};

    const receiverURL = ref("");
    const message = ref("");

    const targetSettings = reactive({
      changedPosition: false,
      alreadyConnected: false,
      followCandidate: false,
    });
    const targetSettingsMessages = {
      changedPosition:
        "Do not send message if current company or position is changed",
      alreadyConnected: "Do not send to people you've already connected with",
      followCandidate: "Follow candidate when sending invite message",
    };
    const previewData = ref('');
    const showPreviewModel = ref(false);
    const preview = () => {
      const previewModel = {
        platform: selectedPlatform,
        sender: selectedSender,
        receiverURL: receiverURL,
        template: selectedTemplate,
        message: message,
        targetSettings: targetSettings,
      };
      previewData.value = JSON.stringify(previewModel);
      showPreviewModel.value = true;
    };
    const closeModel = () => {
      showPreviewModel.value = false;
    }
    const send = () => {
      const sendMessage = {
        platform: selectedPlatform,
        sender: selectedSender,
        receiverURL: receiverURL,
        template: selectedTemplate,
        message: message,
        targetSettings: targetSettings,
      };
      selectedPlatform.value = "";
      selectedSender.value = "";
      receiverURL.value = "";
      selectedTemplate.value = "";
      message.value = "";
      targetSettings.alreadyConnected = false;
      targetSettings.changedPosition = false;
      targetSettings.followCandidate = false;
    }

    return {
      platforms,
      senders,
      templates,
      selectedPlatform,
      selectedSender,
      receiverURL,
      selectedTemplate,
      message,
      targetSettings,
      targetSettingsMessages,
      showPreviewModel,
      previewData,
      filterSendersByPlatforms,
      createAndEditTemplate,
      preview,
      closeModel,
      send,
    };
  },
};
</script>

<style>
.checkbox-message {
  display: flex;
  flex-direction: column;
}
.custom-select {
  width: 35%;
  height: 30px;
}
.custom-textbox {
  width: 90%;
  height: 100px;
}
</style>
