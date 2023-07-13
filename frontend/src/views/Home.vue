<template>
  <!-- このコードではVuetifyを使用してレイアウトを調整している：https://vuetifyjs.com/en/ -->
  <!-- また、コード内容が理解しやすいようにパーツごとのコンポーネント化はせず、あえて単一コンポーネントで実装している -->
  <v-app dark>
    <!-- タイトルを表示するヘッダー部分 -->
    <v-app-bar fixed app class="bg-primary">
      <v-toolbar-title class="text-h4 font-weight-bold text-secondary"
        >Self Introduction</v-toolbar-title
      >
    </v-app-bar>
    <v-spacer />
    <v-main>
      <!-- 取得したプロフィールを表示する部分 -->
      <!-- displayWhichContent変数がprofileの時に表示される -->
      <v-container
        v-if="displayWhichContent == 'profile'"
        class="bg-primary text-secondary"
      >
        <v-row text-align="center" justify="center">
          <v-col cols="10">
            <v-row>
              <v-col
                sm="4"
                md="4"
                lg="4"
                xl="4"
                cols="12"
                class="d-flex flex-column justify-start align-center"
              >
                <img
                  src="../assets/iotan-soracom-sns.png"
                  height="125"
                  max-height="125"
                  width="125"
                  max-width="125"
                />
                <p class="text-h6 font-weight-bold mt-6">
                  {{ profileData.name }}
                </p>
                <v-btn
                  class="mt-4"
                  @click="displayWhichContent = 'edit'"
                  color="setting"
                  variant="outlined"
                  >Edit</v-btn
                >
              </v-col>

              <v-col sm="8" md="8" lg="8" xl="8" cols="12">
                <div>
                  <p class="text-h6 font-weight-bold">Special Skill</p>
                  <p>
                    {{ profileData.skill }}
                  </p>
                </div>
                <div class="mt-6">
                  <p class="text-h6 font-weight-bold">Hobby</p>
                  <ul>
                    <li v-for="hobby in profileData['hobbyList']" :key="hobby">
                      {{ hobby }}
                    </li>
                  </ul>
                </div>
                <div class="mt-6">
                  <p class="text-h6 font-weight-bold">Likes</p>
                  <p>{{ profileData.like }}</p>
                </div>
                <div class="mt-6">
                  <p class="text-h6 font-weight-bold">Comment</p>
                  <p>{{ profileData.comment }}</p>
                </div>
              </v-col>
            </v-row>
          </v-col>
          <v-snackbar v-model="isShownSnackbar" dark top color="error">
            {{ errorMessage }}
          </v-snackbar>
        </v-row>
      </v-container>

      <!-- プロフィールを編集する部分 -->
      <!-- displayWhichContent変数がeditの時に表示される -->
      <v-container v-if="displayWhichContent == 'edit'" class="bg-primary">
        <v-row text-align="center" justify="center">
          <v-col cols="10">
            <v-row>
              <v-col
                sm="4"
                md="4"
                lg="4"
                xl="4"
                cols="12"
                class="d-flex flex-column justify-start"
              >
                　
                <div class="d-flex flex-column align-center">
                  <img
                    src="../assets/iotan-soracom-sns.png"
                    height="125"
                    max-height="125"
                    width="125"
                    max-width="5%"
                  />
                </div>
                <p class="mt-4">
                  <v-text-field
                    v-model="editProfileData.name"
                    :counter="20"
                    label="Name"
                    :rules="[
                      () => !!editProfileData.name || 'Name is required',
                    ]"
                  ></v-text-field>
                </p>
                <div class="d-flex flex-column justify-start align-center">
                  <v-btn
                    class="mt-4"
                    color="success"
                    variant="outlined"
                    @click="saveProfile"
                  >
                    Save
                  </v-btn>
                  <v-btn
                    class="mt-4"
                    color="error"
                    variant="outlined"
                    @click="cancelProfile"
                  >
                    Cancel
                  </v-btn>
                </div>
              </v-col>

              <v-col sm="8" md="8" lg="8" xl="8" cols="12">
                <div>
                  <p class="text-h6 font-weight-bold">Special Skill</p>
                  <v-text-field
                    v-model="editProfileData.skill"
                    :counter="100"
                    label="Special Skill"
                    required
                  ></v-text-field>
                </div>
                <div class="mt-6">
                  <div class="d-flex align-content-start align-end">
                    <p class="text-h6 font-weight-bold">Hobby</p>
                    <v-spacer />
                    <v-icon @click="addHobby" class="text-blue-grey-lighten-1"
                      >mdi-plus-circle-outline</v-icon
                    >
                    <v-icon
                      @click="removeHobby"
                      class="text-blue-grey-lighten-1"
                      >mdi-minus-circle-outline</v-icon
                    >
                  </div>
                  <v-text-field
                    v-for="(hobby, index) in editProfileData.hobbyList"
                    :key="`cdHobby${index}`"
                    v-model="editProfileData.hobbyList[index]"
                    :label="`Hobby${index + 1}`"
                  ></v-text-field>
                </div>
                <div class="mt-6">
                  <p class="text-h6 font-weight-bold">Likes</p>
                  <v-text-field
                    v-model="editProfileData.like"
                    label="like"
                    :counter="100"
                    required
                  ></v-text-field>
                </div>
                <div class="mt-6">
                  <p class="text-h6 font-weight-bold">Comment</p>
                  <v-text-field
                    v-model="editProfileData.comment"
                    label="comment"
                    :counter="100"
                    required
                  ></v-text-field>
                </div>
              </v-col>
            </v-row>
          </v-col>
          <v-snackbar v-model="isShownSnackbar" dark top color="error">
            {{ errorMessage }}
          </v-snackbar>
        </v-row>
      </v-container>
    </v-main>

    <!-- ローディング表示用オーバーレイ -->
    <v-overlay v-model="isLoading" class="justify-center align-center">
      <v-progress-circular
        color="setting"
        :size="100"
        :width="6"
        indeterminate
      ></v-progress-circular>
    </v-overlay>

    <!-- 権利関係を表示するフッター部分 -->
    <v-footer app height="auto">
      <v-col class="text-center py-0">
        <p>Special Thanks <a href="https://qiita.com/papi_tokei/contributions" target="_blank">@papi_tokei</a></p>
        <p>&copy; {{ new Date().getFullYear() }} iot.kyoto all rights reserved.</p>
      </v-col>
    </v-footer>
  </v-app>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted } from "vue";
// AxiosというHTTPライブラリを使用してAPIとの通信を行うためここでimport
// Axios API Reference：https://axios-http.com/docs/api_intro
import axios, { isAxiosError } from "axios";

// 定数の定義
// TODO: エンドポイントとAPIキーを修正する
const URL = "";
const API_KEY = "";
const ID = "1"; // IDは1固定のため定数定義

// axiosのデフォルトヘッダーとしてAPIキーを設定
axios.defaults.headers["X-API-KEY"] = API_KEY;

// プロフィールデータ群の型
interface ProfileData {
  id?: string;
  name: string;
  skill: string;
  hobbyList: string[];
  like: string;
  comment: string;
}

// プロフィールデータ群のオブジェクト
const profileData: ProfileData = reactive({
  name: "",
  skill: "",
  hobbyList: ["", "", ""],
  like: "",
  comment: "",
});

// プロフィール編集用のオブジェクト
const editProfileData: ProfileData = reactive({
  name: "",
  skill: "",
  hobbyList: ["", "", ""],
  like: "",
  comment: "",
});

// ローディング表示のフラグを管理する変数
const isLoading = ref<boolean>(false);
// 画面表示コンテンツを制御するための変数
const displayWhichContent = ref<"profile" | "edit" | "close">("profile");
// 画面に表示するエラーメッセージを格納する変数
const errorMessage = ref<string>("");
// ヘラーメッセージ表示のフラグを管理するための変数
const isShownSnackbar = ref<boolean>(false);

// コンポーネントがマウントされた後に呼び出される内容
// Vueのライフサイクルフック：https://ja.vuejs.org/api/composition-api-lifecycle.html#onmounted
onMounted(() => {
  const load = async () => {
    try {
      displayWhichContent.value = "close";
      isLoading.value = true;
      await getProfile();
      console.log(profileData);
      cancelProfile();
      isLoading.value = false;
      displayWhichContent.value = "profile";
    } catch (err) {
      console.error("エラー：" + err);
      isLoading.value = false;
    }
  };
  load();
});

// DBから取得するデータの型を定義
interface receivedData {
  id: string;
  name: string;
  skill: string;
  "hobby-list": string[];
  like: string;
  comment: string;
}

/**
 * DBからプロフフィール内容を取得し、オブジェクトへ格納する関数
 */
async function getProfile(): Promise<any> {
  try {
    const { data } = await axios.get<receivedData[]>(URL, {
      params: { id: ID },
    });
    profileData.name = data[0].name;
    profileData.skill = data[0].skill;
    profileData.hobbyList = data[0]["hobby-list"];
    profileData.like = data[0].like;
    profileData.comment = data[0].comment;
  } catch (err) {
    if (isAxiosError(err)) {
      console.log(err.message);
      errorMessage.value = "エラー：" + err.message;
      isShownSnackbar.value = true;
    } else {
      console.log(err);
      errorMessage.value = "エラー：" + err;
      isShownSnackbar.value = true;
    }
  }
}

/**
 * 編集したプロフィール内容を送信し、DBを更新する関数
 */
async function saveProfile() {
  try {
    const response = await axios.put(URL, {
      id: ID,
      name: editProfileData.name,
      skill: editProfileData.skill,
      "hobby-list": editProfileData.hobbyList,
      like: editProfileData.like,
      comment: editProfileData.comment,
    });
    console.log("put response:", response);
    await getProfile();
  } catch (err) {
    if (isAxiosError(err)) {
      console.error(err.message);
      errorMessage.value = "エラー：" + err.message;
      isShownSnackbar.value = true;
    } else {
      console.error(err);
      errorMessage.value = "エラー：" + err;
      isShownSnackbar.value = true;
    }
  }
  displayWhichContent.value = "profile";
}

/**
 * キャンセルボタン押下時に編集内容を破棄する関数
 */
function cancelProfile(): void {
  editProfileData.name = profileData.name;
  editProfileData.skill = profileData.skill;
  editProfileData.hobbyList = profileData["hobbyList"].concat();
  editProfileData.like = profileData.like;
  editProfileData.comment = profileData.comment;
  displayWhichContent.value = "profile";
}

/**
 * Hobbyの配列の最後尾に要素を追加する関数
 */
function addHobby(): void {
  editProfileData.hobbyList.push("");
}

/**
 * Hobbyの配列の最後尾の要素を削除する関数
 */
function removeHobby(): void {
  editProfileData.hobbyList.pop();
}
</script>
