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
            :key="platform.id"
            :value="platform"
          >
            {{ platform.name }}
          </option>
        </select>
      </div>

      <div class="select-box">
        <label> User: </label>
        <select class="custom-select" v-model="selectedSender">
          <option disabled selected value="">Choose one user</option>
          <option
            v-for="sender in filterSendersByPlatforms"
            :key="sender.id"
            :value="sender"
          >
            {{ sender.name }}
          </option>
        </select>
      </div>
    </div>

    <div class="receiver-url">
      <label><h3>URL:</h3></label>
      <textarea
        class="custom-textbox"
        v-model="urlReceiver"
        placeholder="Receiver's URL"
      ></textarea>
    </div>

    <div class="message">
      <h3>Message</h3>
      <div class="select-template">
        <div class="item">
          <select class="custom-select" v-model="selectedTemplate">
            <option disabled selected value="undefined">Choose one template</option>
            <option
              v-for="template in templates"
              :key="template.id"
              :value="template.name"
            >
              {{ template.name }}
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
          ref="sampleMessage"
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
        <p>Platform: {{ previewData.platform }}</p>
        <p>Sender: {{ previewData.sender }}</p>
        <p>Receiver URL: {{ previewData.urlReceiver }}</p>
        <p>Message: {{ previewData.message }}</p>
        <p>Choosen target setting:</p>
        <li
          v-for="message in previewData.targetSettings"
          :key="message"
          :value="message"
        >
          {{ message }}
        </li>
        <button @click="send">Send</button>
      </div>
    </div>
  </div>
</template>

<script lang="ts" setup>
import axios from "axios";
import { computed, onMounted, reactive, type Ref, ref } from "vue";

// chọn platform
interface Platform {
  id: number,
  name: string
}
const platforms = ref<Platform[]>();
onMounted(async () => {
  try {
    const response = await axios.get("http://localhost:8000/platforms");
    platforms.value = response.data;
  } catch (error) {
    console.error("Failed to fetch platforms:", error);
  }
});
const selectedPlatform = ref<Platform>();

// chọn sender
interface Sender {
  id: number,
  name: string,
  platform: number,
}

interface SendersData {
  [key: number]: Sender[];
}

const senders: Ref<SendersData> = ref({});

const selectedSender = ref<Sender>();

onMounted(async () => {
  try {
    const response = await axios.get("http://localhost:8000/senders");
    senders.value = response.data;
  } catch (error) {
    console.error("Failed to fetch senders:", error);
  }
});

const filterSendersByPlatforms = computed(() => {
  if (selectedPlatform.value) {
    return senders.value[selectedPlatform.value.id];
  } else {
    return [];
  }
});

// chọn template
interface Template {
  id: number,
  name: string,
  template: string,
}

const templates = ref<Template[]>();
onMounted(async () => {
  try {
    const response = await axios.get<Template[]>("http://localhost:8000/templates");
    templates.value = response.data
  } catch (error) {
    console.error("Failed to fetch templates:", error);
  }
});
const selectedTemplate: Ref<Template | undefined> = ref(undefined);
const createAndEditTemplate = () => {};

// nhập receiver URL và message
const urlReceiver = ref("");
const message = ref("");

// box target setting
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

// xem preview
interface PreviewData {
  platform: string;
  sender: string;
  urlReceiver: string;
  message: string;
  targetSettings: string[];
}

const previewData: Ref<PreviewData> = ref({
  platform: "",
  sender: "",
  urlReceiver: "",
  message: "",
  targetSettings: [],
});
const showPreviewModel = ref(false);
const preview = () => {
  if(selectedPlatform.value)
    previewData.value.platform = selectedPlatform.value.name;
  else
    previewData.value.platform = "Nothing";
  if(selectedSender.value)
    previewData.value.sender = selectedSender.value.name;
  else
    previewData.value.sender = "Nothing";
  if(urlReceiver.value == "")
    previewData.value.urlReceiver = "Nothing";
  else
    previewData.value.urlReceiver = urlReceiver.value;
    
  previewData.value.message = message.value;

  if (
    !targetSettings.alreadyConnected &&
    !targetSettings.changedPosition &&
    !targetSettings.followCandidate
  ) {
    previewData.value.targetSettings.push("Not selected");
  } else {
    if (targetSettings.alreadyConnected) {
      previewData.value.targetSettings.push(
        targetSettingsMessages.alreadyConnected
      );
    }
    if (targetSettings.changedPosition) {
      previewData.value.targetSettings.push(
        targetSettingsMessages.changedPosition
      );
    }
    if (targetSettings.followCandidate) {
      previewData.value.targetSettings.push(
        targetSettingsMessages.followCandidate
      );
    }
  }

  showPreviewModel.value = true;
};
const closeModel = () => {
  previewData.value.targetSettings.splice(0, previewData.value.targetSettings.length);
  showPreviewModel.value = false;
};

// post
interface Message {
  platform: number | undefined;
  receiver: number | undefined;
  urlReceiver: string;
  messageContent: string;
  alreadyConnected: boolean;
  changePosition: boolean;
  followCandidate: boolean;
}

const send = async () => {
  const sendMessage : Message = {
    platform: selectedPlatform.value?.id,
    receiver: selectedSender.value?.id,
    urlReceiver: urlReceiver.value,
    messageContent: message.value,
    alreadyConnected: targetSettings.alreadyConnected,
    changePosition: targetSettings.changedPosition,
    followCandidate: targetSettings.followCandidate,
  };

  try {
    // Gọi API endpoint bằng Axios để gửi thông tin message
    const response = await axios.post(
      "http://localhost:8000/send-message/",
      sendMessage
    );
    console.log(response.data.message); // Hiển thị response từ backend
  } catch (error) {
    console.error("Failed to send message:", error);
  }

  // Đặt giá trị các biến về mặc định sau khi gửi
  selectedPlatform.value = undefined;
  selectedSender.value = undefined;
  urlReceiver.value = "";
  selectedTemplate.value = undefined;
  message.value = "";
  targetSettings.alreadyConnected = false;
  targetSettings.changedPosition = false;
  targetSettings.followCandidate = false;
  previewData.value.targetSettings.splice(0, previewData.value.targetSettings.length);
  showPreviewModel.value = false;
};
</script>

<style>
.checkbox-message {
  display: flex;
  flex-direction: column;
}

.custom-textbox {
  resize: none;
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
  margin-bottom: 10px;
}

.select-platform-and-sender {
  display: flex;
  margin-top: 10px;
  margin-bottom: 10px;
}

.select-platform-and-sender .custom-select {
  width: 60%;
  height: 30px;
}

.select-template {
  display: flex;
  margin-top: 10px;
  margin-bottom: 10px;
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
  display: flex;
  justify-content: center;
  align-items: center;
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.5); /* Màu nền xám mờ */
  z-index: 9999;
}

.popup-content {
  width: 50%;
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  background-color: white;
  padding: 20px;
  border-radius: 10px;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.2);
}

.close {
  position: absolute;
  top: 10px;
  right: 10px;
  font-size: 20px;
  cursor: pointer;
}

h3 {
  margin-top: 0;
}

p {
  margin: 5px 0;
}

ul {
  list-style: none;
  padding: 0;
  margin: 5px 0;
}

li {
  margin: 3px 0;
}
</style>
