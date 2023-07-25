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
        <p>Platform: {{ previewData.platform }}</p>
        <p>Sender: {{ previewData.sender }}</p>
        <p>Receiver URL: {{ previewData.receiverURL }}</p>
        <p>Template: {{ previewData.template }}</p>
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
const platforms = ref([]);
onMounted(async () => {
  try {
    const response = await axios.get("http://localhost:8000/platforms");
    platforms.value = response.data;
  } catch (error) {
    console.error("Failed to fetch platforms:", error);
  }
});
const selectedPlatform = ref("");

// chọn sender
interface SendersData {
  [key: string]: string[];
}

const senders: Ref<SendersData> = ref({});

const selectedSender = ref("");

const filterSendersByPlatforms = computed(() => {
  return senders.value[selectedPlatform.value] || []; // Sử dụng senders.value thay vì senders
});

onMounted(async () => {
  try {
    const response = await axios.get("http://localhost:8000/senders");
    senders.value = response.data; // Gán dữ liệu trực tiếp cho senders.value
  } catch (error) {
    console.error("Failed to fetch senders:", error);
  }
});

// chọn template
const templates = ref([]);
onMounted(async () => {
  try {
    const response = await axios.get("http://localhost:8000/templates");
    templates.value = response.data; // Gán dữ liệu trực tiếp cho senders.value
  } catch (error) {
    console.error("Failed to fetch templates:", error);
  }
});
const selectedTemplate = ref("");
const createAndEditTemplate = () => {};

// nhập receiver URL và message
const receiverURL = ref("");
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
const previewData = ref({
  platform: "",
  sender: "",
  receiverURL: "",
  template: "",
  message: "",
  targetSettings: [""],
});
const showPreviewModel = ref(false);
const preview = () => {
  previewData.value.platform = selectedPlatform.value;
  previewData.value.sender = selectedSender.value;
  previewData.value.receiverURL = receiverURL.value;
  previewData.value.template = selectedTemplate.value;
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
// const send = () => {
//   const sendMessage = {
//     platform: selectedPlatform,
//     sender: selectedSender,
//     receiverURL: receiverURL,
//     template: selectedTemplate,
//     message: message,
//     targetSettings: targetSettings,
//   };
//   selectedPlatform.value = "";
//   selectedSender.value = "";
//   receiverURL.value = "";
//   selectedTemplate.value = "";
//   message.value = "";
//   targetSettings.alreadyConnected = false;
//   targetSettings.changedPosition = false;
//   targetSettings.followCandidate = false;
//   showPreviewModel.value = false;
// };

const send = async () => {
  const sendMessage = {
    platform: selectedPlatform.value,
    sender: selectedSender.value,
    receiverURL: receiverURL.value,
    template: selectedTemplate.value,
    message: message.value,
    targetSettings: targetSettings,
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
