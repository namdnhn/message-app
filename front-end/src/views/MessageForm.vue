<template>
  <Header></Header>
  <div class="custom-background">
    <div style="margin-top: 10px; margin-bottom: 20px">
      <h2 style="font: Verdana">Message</h2>
    </div>

    <div class="select-platform-and-sender">
      <div class="select-box">
        <label>
          <div class="header-label">
            <h6 style="margin: 2.5px 0px">Platform</h6>
            <div class="rectangle"><b>Required</b></div>
          </div>
        </label>
        <select class="custom-select" v-model="selectedPlatform" required>
          <option disabled selected value="undefined">
            Choose one platform
          </option>
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
        <label>
          <div class="header-label">
            <h6 style="margin: 2.5px 0px">Sender</h6>
            <div class="rectangle"><b>Required</b></div>
          </div>
        </label>
        <select class="custom-select" v-model="selectedSender" required>
          <option disabled selected value="undefined">Choose one user</option>
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
      <label
        ><div class="header-label">
          <h6 style="margin: 2.5px 0px">Receiver's URL</h6>
          <div class="rectangle"><b>Required</b></div>
        </div></label
      >
      <textarea
        class="custom-textbox"
        v-model="urlReceiver"
        placeholder="Receiver's URL"
        required
      ></textarea>
    </div>

    <div class="message">
      <h6>Message</h6>
      <div class="select-template">
        <div class="item">
          <select
            class="custom-select"
            @change="onChangeTemplate"
            :value="selectedTemplateId"
          >
            <option disabled selected value="0">Choose one template</option>
            <option
              v-for="template in templates"
              :key="template.id"
              :value="template.id"
            >
              {{ template.name }}
            </option>
          </select>
        </div>

        <div class="item">
          <button
            class="create-and-edit-template-button"
            @click="createAndEditTemplate"
          >
            Create and Edit Template
          </button>
        </div>
      </div>
      <div class="place-holder">
        <label>
          <p style="font-size: x-small; margin-left: 10px; margin-bottom: 5px">
            Placeholder
          </p>
        </label>
        <div class="place-holder-order">
          <button
            class="place-holder-button"
            v-for="option in placeholderOptions"
            :key="option.name"
            @click="addPlaceholder(option.text)"
          >
            {{ option.name }}
          </button>
        </div>
      </div>
      <div class="header-label">
        <div
          style="
            height: 17px;
            width: 42px;
            align-items: center;
            border: 2px solid red;
            margin-top: 5px;
            margin-bottom: 10px;
            font-size: 9px;
            color: red;
          "
        >
          <b>Required</b>
        </div>
      </div>
      <div class="message-box">
        <textarea
          class="custom-textbox"
          v-model="message"
          placeholder="Message"
          required
        ></textarea>
      </div>
    </div>

    <h6>Target Settings</h6>
    <div class="checkbox-message">
      <label style="font-size: smaller; margin: 5px; font-weight: bold">
        <input type="checkbox" v-model="targetSettings.changedPosition" />
        {{ targetSettingsMessages.changedPosition }}
      </label>
      <label style="font-size: smaller; margin: 5px; font-weight: bold">
        <input type="checkbox" v-model="targetSettings.alreadyConnected" />
        {{ targetSettingsMessages.alreadyConnected }}
      </label>
      <label style="font-size: smaller; margin: 5px; font-weight: bold">
        <input type="checkbox" v-model="targetSettings.followCandidate" />
        {{ targetSettingsMessages.followCandidate }}
      </label>
    </div>

    <div class="check-validate">
      <p v-if="!checkSelectedPlatform">
        You must choose platform before send message
      </p>
      <p v-if="!checkSelectedSender">
        You must choose a sender before send message
      </p>
      <p v-if="!checkReceiverURL">The Receiver URL box can not be empty</p>
      <p v-if="!checkMessage">The message box can not be empty</p>
    </div>
    <button
      class="preview-and-send-button"
      style="margin-top: 5px"
      @click="preview"
      :disabled="
        !checkMessage ||
        !checkReceiverURL ||
        !checkSelectedPlatform ||
        !checkSelectedSender
      "
    >
      Preview and Send
    </button>

    <div v-if="showPreviewModel" class="popup">
      <div class="popup-content">
        <span class="close" @click="closeModel">&times;</span>
        <h3>Preview</h3>
        <table class="config-table">
          <tr>
            <th>Platform</th>
            <td>{{ previewData.platform }}</td>
          </tr>
          <tr>
            <th>Receiver URL</th>
            <td>{{ previewData.urlReceiver }}</td>
          </tr>
          <tr>
            <th>Sender</th>
            <td>{{ previewData.sender }}</td>
          </tr>
          <tr>
            <th>Message</th>
            <td>
              <textarea
                disabled
                class="custom-textbox"
                :value="message"
                required
              ></textarea>
            </td>
          </tr>
          <tr>
            <th>Choosen target setting</th>
            <td>
              <li
                v-for="message in previewData.targetSettings"
                :key="message"
                :value="message"
                style="font-weight: bold"
              >
                {{ message }}
              </li>
            </td>
          </tr>
        </table>
        <button class="preview-and-send-button" @click="send">Send</button>
        <button class="create-and-edit-template-button" @click="closeModel">
          Back
        </button>
      </div>
    </div>

    <div v-if="showCreateAndEditTemplate" class="popup">
      <div class="popup-content">
        <TabWrapper>
          <Tab title="Create">
            <span class="close" @click="closeTemplate">&times;</span>
            <h3>Create Template</h3>
            <table class="config-table">
              <tr>
                <th>Template name</th>
                <td>
                  <input
                    v-model="newTemplateName"
                    class="custom-input"
                    placeholder="Template name"
                  />
                </td>
              </tr>
              <tr>
                <th>Template content</th>
                <td>
                  <textarea
                    v-model="newTemplateContent"
                    class="custom-textbox-template-content"
                    placeholder="Template content"
                  ></textarea>
                </td>
              </tr>
            </table>
            <div class="check-validate">
              <p v-if="!checkNewTemplateName">
                The Template Name box can not be empty
              </p>
              <p v-if="!checkNewTemplateContent">
                The Template Content box can not be empty
              </p>
            </div>
            <div>
              <button
                class="preview-and-send-button"
                @click="saveTemplate"
                :disabled="!checkNewTemplateName || !checkNewTemplateContent"
              >
                Save
              </button>
              <button
                class="create-and-edit-template-button"
                @click="closeTemplate"
              >
                Back
              </button>
            </div>
          </Tab>
          <Tab title="Edit">
            <span class="close" @click="closeTemplate">&times;</span>
            <h3>Edit Template</h3>
            <table class="config-table">
              <tr>
                <th>Choose Template</th>
                <td>
                  <select
                    class="custom-select-edit-template"
                    @change="onChangeEditTemplate"
                    :value="selectedTemplateToEditId"
                  >
                    <option
                      v-for="template in templates"
                      :key="template.id"
                      :value="template.id"
                    >
                      {{ template.name }}
                    </option>
                  </select>
                </td>
              </tr>
              <tr>
                <th>Template name</th>
                <td>
                  <input
                    v-model="editTemplateName"
                    class="custom-input"
                    placeholder="Template name"
                    :disabled="selectedTemplateToEditId === 0"
                  />
                </td>
              </tr>
              <tr>
                <th>Template content</th>
                <td>
                  <textarea
                    v-model="editTemplateContent"
                    class="custom-textbox-template-content"
                    placeholder="Template content"
                    :disabled="selectedTemplateToEditId === 0"
                  ></textarea>
                </td>
              </tr>
            </table>
            <div class="check-validate">
              <p v-if="!checkSelectedTemplateToEdit">
                You must choose a template to edit
              </p>
              <p v-if="!checkEditTemplateName">
                The Template Name box can not be empty
              </p>
              <p v-if="!checkEditTemplateContent">
                The Template Content box can not be empty
              </p>
            </div>
            <div>
              <button
                class="preview-and-send-button"
                @click="editTemplate"
                :disabled="
                  !checkSelectedTemplateToEdit ||
                  !checkEditTemplateName ||
                  !checkEditTemplateContent
                "
              >
                Save
              </button>
              <button
                class="delete-button"
                @click="deleteTemplate"
                :disabled="!checkSelectedTemplateToEdit"
              >
                Delete
              </button>
            </div>
          </Tab>
        </TabWrapper>
      </div>
    </div>
  </div>
</template>

<script lang="ts" setup>
import axios from "axios";
import { computed, onMounted, reactive, type Ref, ref, watch } from "vue";
import TabWrapper from "@/components/tab/TabWrapper.vue";
import Tab from "@/components/tab/Tab.vue";
import Header from "@/components/Header.vue";

const components = { Tab, TabWrapper, Header };

// chọn platform
interface Platform {
  id: number;
  name: string;
}
const platforms = ref<Platform[]>();

const fetchPlatforms = async () => {
  try {
    const response = await axios.get("http://localhost:8000/platforms");
    platforms.value = response.data;
  } catch (error) {
    console.error("Lỗi khi lấy thông tin các nền tảng:", error);
  }
};

const selectedPlatform = ref<Platform>();
const checkSelectedPlatform = computed(() => {
  if (selectedPlatform.value != undefined) return true;
  else return false;
});

// chọn sender
interface Sender {
  id: number;
  name: string;
  platform: number;
}

interface PlatformSenderList {
  [key: number]: Sender[];
}

const senders: Ref<PlatformSenderList> = ref({});

const selectedSender = ref<Sender>();

const fetchSenders = async () => {
  try {
    const response = await axios.get("http://localhost:8000/senders");
    senders.value = response.data;
  } catch (error) {
    console.error("Lỗi khi lấy thông tin người gửi:", error);
  }
};

const filterSendersByPlatforms = computed(() => {
  if (selectedPlatform.value) {
    return senders.value[selectedPlatform.value.id];
  } else {
    return [];
  }
});

const checkSelectedSender = computed(() => {
  if (selectedSender.value != undefined) return true;
  else return false;
});

// chọn template
interface SendTemplateRequest {
  name: string;
  template: string;
}

interface GetTemplateRequest {
  id: number;
  name: string;
  template: string;
}

const showCreateAndEditTemplate = ref(false);
const templates: Ref<GetTemplateRequest[]> = ref([]);

const fetchTemplates = async () => {
  try {
    const response = await axios.get("http://localhost:8000/templates");
    templates.value = response.data;
  } catch (error) {
    console.error("Lỗi khi lấy thông tin các mẫu:", error);
  }
};

onMounted(() => {
  fetchPlatforms();
  fetchSenders();
  fetchTemplates();
});

const selectedTemplateId: Ref<number> = ref(0);
const templateFilterById = computed(() => {
  return templates.value.find(
    (template) => template.id == selectedTemplateId.value
  );
});

const templateToEditFilterById = computed(() => {
  return templates.value.find(
    (template) => template.id == selectedTemplateToEditId.value
  );
});

const onChangeTemplate = (event: { target: { value: number } }) => {
  selectedTemplateId.value = event.target.value;
  message.value = templateFilterById.value?.template || "";
};
const createAndEditTemplate = () => {
  showCreateAndEditTemplate.value = true;
};
const closeTemplate = () => {
  showCreateAndEditTemplate.value = false;
};

// create Template
const newTemplateName = ref("");
const newTemplateContent = ref("");
const checkNewTemplateName = computed(() => {
  return newTemplateName.value != "";
});
const checkNewTemplateContent = computed(() => {
  return newTemplateContent.value != "";
});
const saveTemplate = async () => {
  const newTemplate: SendTemplateRequest = {
    name: newTemplateName.value,
    template: newTemplateContent.value,
  };
  try {
    const response = await axios.post(
      "http://localhost:8000/create-templates/",
      newTemplate
    );
    window.alert("Tạo template " + response.data.name + " thành công");
    fetchTemplates();
  } catch (error) {
    console.error("Failed to send message:", error);
  }
  newTemplateName.value = "";
  newTemplateContent.value = "";
  showCreateAndEditTemplate.value = false;
};

// edit Template
const editTemplateName = ref("");
const editTemplateContent = ref("");
const selectedTemplateToEditId: Ref<number> = ref(0);

const checkEditTemplateName = computed(() => {
  return editTemplateName.value != "";
});
const checkEditTemplateContent = computed(() => {
  return editTemplateContent.value != "";
});
const checkSelectedTemplateToEdit = computed(() => {
  return selectedTemplateToEditId.value != 0;
});

// delete Template
const deleteTemplate = async () => {
  if (selectedTemplateToEditId.value == 0) {
    return;
  }
  try {
    // Gọi API endpoint bằng Axios để gửi thông tin message
    const response = await axios.delete(
      "http://localhost:8000/delete-templates/" + selectedTemplateToEditId.value
    );
    window.alert("Xóa template " + response.data.id + " thành công");
    fetchTemplates();
    // console.log(response.data.message); // Hiển thị response từ backend
  } catch (error) {
    console.error("Failed to send message:", error);
  }
  editTemplateName.value = "";
  editTemplateContent.value = "";
  showCreateAndEditTemplate.value = false;
};

const editTemplate = async () => {
  if (selectedTemplateToEditId.value == 0) {
    return;
  }
  const newTemplate: SendTemplateRequest = {
    name: editTemplateName.value,
    template: editTemplateContent.value,
  };
  try {
    // Gọi API endpoint bằng Axios để gửi thông tin message
    const response = await axios.put(
      "http://localhost:8000/edit-templates/" + selectedTemplateToEditId.value,
      newTemplate
    );
    window.alert("Chỉnh sửa template " + response.data.name + " thành công");
    fetchTemplates();
  } catch (error) {
    console.error("Failed to send message:", error);
  }
  editTemplateName.value = "";
  editTemplateContent.value = "";
  showCreateAndEditTemplate.value = false;
};

const onChangeEditTemplate = (event: { target: { value: number } }) => {
  selectedTemplateToEditId.value = event.target.value;
  editTemplateName.value = templateToEditFilterById.value?.name || "";
  editTemplateContent.value = templateToEditFilterById.value?.template || "";
};

// nhập receiver URL và message
const placeholderOptions = [
  { name: "candidate", text: " #__CANDIDATE__# " },
  { name: "platform", text: " #__PLATFORM__# " },
  { name: "age", text: " #__AGE__# " },
];
const addPlaceholder = (text: string) => {
  message.value += text;
};
const urlReceiver = ref("");
const message: Ref<string> = ref("");

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

// check validate
const validateData = computed(() => {
  return (
    checkMessage &&
    checkReceiverURL &&
    checkSelectedPlatform &&
    checkSelectedSender
  );
});

const checkReceiverURL = computed(() => {
  if (urlReceiver.value != "") return true;
  else return false;
});

const checkMessage = computed(() => {
  if (message.value != "") return true;
  else return false;
});

// xem preview
interface PreviewData {
  platform: string;
  sender: string;
  urlReceiver: string;
  message: string;
  targetSettings: string[];
}

const previewData: PreviewData = reactive({
  platform: "",
  sender: "",
  urlReceiver: "",
  message: "",
  targetSettings: [],
});
const showPreviewModel = ref(false);
const preview = () => {
  if (!validateData.value) {
    return;
  }
  if (selectedPlatform.value)
    previewData.platform = selectedPlatform.value.name;
  else previewData.platform = "Nothing";
  if (selectedSender.value) previewData.sender = selectedSender.value.name;
  else previewData.sender = "Nothing";
  if (urlReceiver.value == "") previewData.urlReceiver = "Nothing";
  else previewData.urlReceiver = urlReceiver.value;

  previewData.message = message.value;

  if (
    !targetSettings.alreadyConnected &&
    !targetSettings.changedPosition &&
    !targetSettings.followCandidate
  ) {
    previewData.targetSettings.push("Not selected");
  } else {
    if (targetSettings.alreadyConnected) {
      previewData.targetSettings.push(targetSettingsMessages.alreadyConnected);
    }
    if (targetSettings.changedPosition) {
      previewData.targetSettings.push(targetSettingsMessages.changedPosition);
    }
    if (targetSettings.followCandidate) {
      previewData.targetSettings.push(targetSettingsMessages.followCandidate);
    }
  }
  showPreviewModel.value = true;
};
const closeModel = () => {
  editTemplateContent.value = "";
  editTemplateName.value = "";
  selectedTemplateToEditId.value = 0;
  previewData.targetSettings.splice(0, previewData.targetSettings.length);
  showPreviewModel.value = false;
};

// post
interface SendMessageRequest {
  platform?: number;
  receiver?: number;
  urlReceiver: string;
  messageContent: string;
  alreadyConnected: boolean;
  changePosition: boolean;
  followCandidate: boolean;
}

const send = async () => {
  const sendMessage: SendMessageRequest = {
    platform: selectedPlatform.value?.id,
    receiver: selectedSender.value?.id,
    urlReceiver: urlReceiver.value,
    messageContent: message.value,
    alreadyConnected: targetSettings.alreadyConnected,
    changePosition: targetSettings.changedPosition,
    followCandidate: targetSettings.followCandidate,
  };

  try {
    const response = await axios.post(
      "http://localhost:8000/create-messages/",
      sendMessage
    );
    // Đặt giá trị các biến về mặc định sau khi gửi
    selectedPlatform.value = undefined;
    selectedSender.value = undefined;
    urlReceiver.value = "";
    selectedTemplateId.value = 0;
    message.value = "";
    targetSettings.alreadyConnected = false;
    targetSettings.changedPosition = false;
    targetSettings.followCandidate = false;
    previewData.targetSettings.splice(0, previewData.targetSettings.length);
  } catch (error) {
    window.alert("Failed to send message: " + error);
  }

  showPreviewModel.value = false;
};
</script>

<style>
.custom-background {
  width: 70%;
  margin: 10px auto;
  border: 1px solid #999;
  padding: 35px;
  border-radius: 10px;
  background-color: white;
  box-shadow: 0px 2px 10px grey;
}

.checkbox-message {
  display: flex;
  flex-direction: column;
}

.custom-input {
  border: 2px solid #999;
  border-radius: 5px;
  width: 90%;
}

.custom-textbox {
  border-radius: 5px;
  resize: none;
  width: 100%;
  height: 100px;
}

.custom-textbox-template-content {
  border: 2px solid #999;
  border-radius: 5px;
  resize: none;
  width: 90%;
  height: 120px;
}

.create-and-edit-template-button {
  height: 30px;
  border-color: blue;
  background-color: white;
  color: blue;
  font-weight: bold;
  align-items: center;
  margin-right: 20px;
  border-radius: 5px;
  transition-duration: 0.4s;
}

.create-and-edit-template-button:hover {
  border-color: red;
  color: red;
}

.message {
  margin-top: 10px;
  margin-bottom: 10px;
}

::placeholder {
  color: #999;
}

.receiver-url {
  display: flex;
  flex-direction: column;
  margin-top: 20px;
  margin-bottom: 20px;
}

.select-platform-and-sender {
  display: flex;
  margin-top: 20px;
  margin-bottom: 20px;
}

.select-platform-and-sender .custom-select {
  border-radius: 5px;
  width: 70%;
  height: 30px;
  cursor: pointer;
  display: inline-block;
  font-size: 16px;
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
  border-radius: 5px;
  width: 70%;
  height: 30px;
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
  width: 75%;
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  background-color: white;
  padding: 30px;
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

.place-holder {
  background-color: rgb(216, 216, 216);
  margin-bottom: 5px;
}

.place-holder-button {
  height: 20px;
  align-items: center;
  font-size: x-small;
  border-color: blue;
  background-color: blue;
  color: white;
  font-weight: bold;
  margin-left: 10px;
  margin-right: 10px;
  margin-bottom: 10px;
  border-radius: 5px;
  transition-duration: 0.4s;
}

.place-holder-button:hover {
  border-color: rgb(122, 122, 255);
  background-color: rgb(122, 122, 255);
}

.custom-select-edit-template {
  border: 2px solid #999;
  border-radius: 5px;
}

.rectangle {
  height: 17px;
  width: 42px;
  border: 2px solid red;
  margin: 5px;
  align-items: center;
  font-size: 9px;
  color: red;
}

.header-label {
  display: flex;
}

.preview-and-send-button {
  height: 30px;
  margin: 0% 42.5%;
  border-color: orange;
  background-color: orange;
  color: white;
  font-weight: bold;
  align-items: center;
  margin-right: 20px;
  border-radius: 5px;
  transition-duration: 0.4s;
}

.preview-and-send-button:hover {
  border-color: rgb(250, 197, 98);
  background-color: rgb(250, 197, 98);
  color: white;
}

.preview-and-send-button:disabled {
  border-color: rgb(250, 232, 197);
  background-color: rgb(232, 215, 184);
  color: white;
}

.config-table {
  width: 100%;
  margin: 20px;
}

.config-table th {
  /* border: 1px solid black; */
  width: 25%;
  padding: 10px;
  font-weight: bold;
  color: #666464;
}

.config-table td {
  /* border: 1px solid black; */
  width: 75%;
  padding: 10px;
  font-weight: bold;
}

.check-validate {
  text-align: center;
  color: red;
  font-size: x-small;
  line-height: 0.5px;
  margin-top: 10px;
}

.delete-button {
  height: 30px;
  border-color: red;
  background-color: white;
  color: red;
  font-weight: bold;
  align-items: center;
  margin-right: 20px;
  border-radius: 5px;
  transition-duration: 0.4s;
}

.delete-button:hover {
  border-color: rgb(168, 2, 2);
  color: rgb(168, 2, 2);
}

.delete-button:disabled {
  border-color: rgb(255, 134, 134);
  color: rgb(255, 134, 134);
}
h3 {
  font: Verdana;
  margin-top: 0;
}

p {
  font: Verdana;
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
select {
  cursor: pointer;
  display: inline-block;
  position: relative;
  font-size: 16px;
  color: black;
  width: auto;
  height: auto;
}
</style>
