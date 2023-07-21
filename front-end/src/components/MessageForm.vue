<template>
  <div class="custom-background">
    <h1>Message</h1>
    <div class="select-platform-and-sender">
      <div class="select-box">
        <label>Platform: </label>
        <select class="custom-select" v-model="selectedPlatform">
          <option disabled selected value="">Choose one platform</option>
          <option
            v-for="platform in platforms"
            :key="platform"
            :value="platform"
          >
            {{ platform }}
          </option>
        </select>
      </div>

      <div class="select-box">
        <label> User: </label>
        <select class="custom-select" v-model="selectedSender">
          <option disabled selected value="">Choose one user</option>
          <option
            v-for="sender in filterSendersByPlatforms"
            :key="sender"
            :value="sender"
          >
            {{ sender }}
          </option>
        </select>
      </div>
    </div>

    <div class="receiver-url">
      <label><h3>URL:</h3></label>
      <textarea
        class="custom-textbox"
        type="text"
        v-mode="receiverURL"
        placeholder="ReceiverURL"
      ></textarea>
    </div>

    <div class="message">
      <h3>Message</h3>
      <div class="select-template">
        <div class="item">
          <select class="custom-select" v-model="selectedTemplate">
            <option disabled selected value="">Choose one template</option>
            <option
              v-for="template in templates"
              :key="template"
              :value="template"
            >
              {{ template }}
            </option>
          </select>
        </div>

        <div class="item">
          <button class="create-template" @click="createAndEditTemplate">
            Create and Edit Template
          </button>
        </div>
      </div>
      <div class="message-box">
        <textarea
          class="custom-textbox"
          v-model="message"
          placeholder="Message"
        ></textarea>
      </div>
    </div>

    <h3>Target Settings</h3>
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

    <div v-if="showPreviewModel" class="popup">
      <div class="popup-content">
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
    const previewData = ref("");
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
    };
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
      showPreviewModel.value = false;
    };

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

.custom-textbox {
  width: 90%;
  height: 100px;
}

.message {
  margin-top: 10px;
  margin-bottom: 10px;
}

::placeholder {
  color: #999; /* Định dạng màu cho chữ placeholder, ví dụ: xám nhạt (#999) */
}

.receiver-url {
  display: flex;
  flex-direction: column;
  margin-top: 10px;
  margin-bottom:10px;
}

.select-platform-and-sender {
  display: flex;
  margin-top: 10px;
  margin-bottom:10px;
}

.select-platform-and-sender .custom-select {
  width: 60%;
  height: 30px;
}

.select-template {
  display: flex;
  margin-top: 10px;
  margin-bottom:10px;
}

.select-template .item {
  flex: 1;
}

.select-template .custom-select {
  width: 60%;
  height: 30px;
}

.select-template .create-template {
  height: 30px;
  align-items: center;
  display: flex;
}

.select-box {
  width: 50%;
  display: flex;
  flex-direction: column;
}

.popup {
  display: none; /* Mặc định ẩn popup */
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.5); /* Hiệu ứng mờ nền */
}

.popup-content {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  background-color: white;
  padding: 20px;
  border-radius: 5px;
}

.close {
  position: absolute;
  top: 10px;
  right: 10px;
  font-size: 20px;
  cursor: pointer;
}
</style>
