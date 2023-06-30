<template>
  <v-app dark>
    <v-app-bar fixed app>
      <v-toolbar-title>Self Introduction</v-toolbar-title>
      <v-spacer />
    </v-app-bar>

    <v-main>
      <v-container>
        <v-row align="center" justify="center">
          <v-col cols="10">
            <v-row class="main_contents">
              <v-col sm="4" md="4" lg="4" xl="4" cols="12" class="d-flex flex-column justify-start align-center">
                <img src="./assets/icon.png" height="125" max-height="125" width="125" max-width="125" />
                <h3 class="mt-6">{{ dataItem.profileData.name }}</h3>
                <v-btn dark class="mt-4" @click="dataItem.dialog = true">Edit</v-btn>
              </v-col>

              <v-col sm="8" md="8" lg="8" xl="8" cols="12">
                <div>
                  <h3>Special Skill</h3>
                  <p>
                    {{ dataItem.profileData.skill }}
                  </p>
                </div>
                <div class="mt-6">
                  <h3>Hobby</h3>
                  <ul>
                    <li v-for="hobby in dataItem.profileData['hobby-list']" :key="hobby">{{ hobby }}</li>
                  </ul>
                </div>
                <div class="mt-6">
                  <h3>Likes</h3>
                  <P>{{ dataItem.profileData.like }}</P>
                </div>
                <div class="mt-6">
                  <h3>Comment</h3>
                  <p>{{ dataItem.profileData.comment }}</p>
                </div>
              </v-col>
            </v-row>
          </v-col>

          <v-dialog v-model="dataItem.dialog" persistent max-width="450">
            <v-card>
              <v-card-title class="headline">Edit Your Profile</v-card-title>
              <v-card-text>
                <v-form ref="form" lazy-validation>
                  <v-text-field v-model="dataItem.editName" :counter="20" label="Name" required></v-text-field>
                  <v-text-field v-model="dataItem.editSkill" :counter="100" label="Special Skill" required></v-text-field>
                  <v-text-field v-for="(hobby, index) in dataItem.editHobby" :key="`cdHobby${index}`"
                    v-model="dataItem.editHobby[index]" :label="`Hobby${index}`" required></v-text-field>
                  <v-text-field v-model="dataItem.editLike" label="like" :counter="100" required></v-text-field>
                  <v-text-field v-model="dataItem.editComment" label="comment" :counter="100" required></v-text-field>
                </v-form>
              </v-card-text>
              <v-card-actions>
                <v-spacer></v-spacer>
                <v-btn color="red darken-1" text @click="cancelProfile">
                  Cancel
                </v-btn>
                <v-btn color="green darken-1" text @click="saveProfile">
                  Save
                </v-btn>
              </v-card-actions>
            </v-card>
          </v-dialog>
          <v-snackbar v-model="dataItem.snackbar" dark top color="error">
            {{ dataItem.errorMessage }}
          </v-snackbar>
        </v-row>
      </v-container>
    </v-main>

    <v-footer app height="32">
      <v-col class="text-center py-0">&copy; {{ new Date().getFullYear() }} papi-tokei all rights
        reserved.</v-col>
    </v-footer>
  </v-app>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import axios from 'axios'
// import { SelfIntroductionMainInterface } from "../types/main";

// TODO: エンドポイントを修正する
const URL =
  "https://ml1hiztzw3.execute-api.ap-northeast-1.amazonaws.com/prod/user-data";


const dataItem = ref(
  {
    dialog: false,
    snackbar: false,
    errorMessage: "",
    name: "Taro Tanaka",
    skill: "特技は特にありません。",
    hobbyList: ["Dead by Daylight", "寝ること", "走ること"],
    like: "食べ物に好き嫌いはありません。",
    comment: "よろしくお願いします。",
    editName: "",
    editSkill: "",
    editHobby: ["", "", ""],
    editLike: "",
    editComment: "",
    profileData: {
      id: "",
      name: "Taro Tanaka",
      skill: "特技は特にありません。",
      "hobby-list": ["Dead by Daylight", "寝ること", "走ること"],
      like: "食べ物に好き嫌いはありません。",
      comment: "よろしくお願いします。"
    }
  }
)

onMounted(() => {
  // const error = ref(null)

  const load = async () => {
    try {
      const { data } = await axios.post(URL, { method: "get" });
      console.log(data); //statusが OKか確認する。
      dataItem.value.profileData = data[0];
      console.log(dataItem.value.profileData);
      // updateData();
      cancelProfile();
    } catch (err) {
      console.log("エラー：" + err);
    }
  }
  load();
})

function cancelProfile() {
  dataItem.value.editName = dataItem.value.profileData.name;
  dataItem.value.editSkill = dataItem.value.profileData.skill;
  dataItem.value.editHobby = dataItem.value.profileData["hobby-list"].concat();
  dataItem.value.editLike = dataItem.value.profileData.like;
  dataItem.value.editComment = dataItem.value.profileData.comment;
  dataItem.value.dialog = false;
}

async function saveProfile() {
  try {
    await axios.post(URL, {
      method: "update",
      data: {
        id: "1",
        name: dataItem.value.editName,
        skill: dataItem.value.editSkill,
        "hobby-list": dataItem.value.editHobby,
        like: dataItem.value.editLike,
        comment: dataItem.value.editComment
      }
    });
    // eslint-disable-next-line @typescript-eslint/no-explicit-any
    const { data } = await axios.post(URL, { method: "get" });
    dataItem.value.profileData = data[0];
    // updateData();
  } catch (err) {
    dataItem.value.errorMessage = "エラー：" + err;
    dataItem.value.snackbar = true;
  }

  dataItem.value.dialog = false;
}

function updateData() {
  if (dataItem.value.profileData) {
    dataItem.value.name = dataItem.value.profileData.name;
    dataItem.value.skill = dataItem.value.profileData.skill;
    dataItem.value.hobbyList = dataItem.value.profileData["hobby-list"];
    dataItem.value.like = dataItem.value.profileData.like;
    dataItem.value.comment = dataItem.value.profileData.comment;
  }
}
</script>

<style scoped>
* {
  margin: 0;
}

body {
  background-color: #F0F0E0;
}

header {
  background-color: #8DB2BA;
  display: flex;
}

div {
  color: #F0F0E0;
  background-color: #edb5b5;
}

.flex-container {
  display: flex;
  padding: 10px;
  /* 枠線を見えるようにする */
  border: solid;
  /* 枠線の色指定 */
  border-color: #F0F0E0;
  height: max-content;
  margin: 100px;
}

.left {
  text-align: center;
  flex-basis: 30%;
  display: flex;
  flex-direction: column;
  justify-content: center;
}

img {
  border: 3px solid #F0F0E0;
  border-radius: 50%;
  width: 180px;
  height: 180px;
  object-fit: cover;
}

.title {
  padding: 10px 20px;
  display: inline-block;
  font-size: xx-large;
}

.name {
  padding: 10px 20px;
  display: flex;
  justify-content: center;
  font-size: x-large;
}

.fam-name {
  display: inline;
  background-color: #F0F0E0;
  color: #edb5b5;
  border: 2px solid #F0F0E0;
  padding: 2px 10px;
  padding-right: 5px;
}

.fst-name {
  display: inline;
  border: 2px solid #F0F0E0;
  padding: 2px 10px;
  padding-left: 5px;
}

.right {
  display: flex;
  flex-flow: column;
  flex-basis: 70%;
}

.content {
  font-size: large;
}

.header {
  margin: 0 auto;
  display: flex;
}




/* チェックボックスを非表示にする */
.drawer_hidden {
  display: none;
}

/* ハンバーガーアイコンの設置スペース */
.drawer_open {
  display: flex;
  height: 60px;
  width: 60px;
  justify-content: center;
  align-items: center;
  position: relative;
  z-index: 100;
  /* 重なり順を一番上にする */
  cursor: pointer;
}

/* ハンバーガーメニューのアイコン */
.drawer_open span,
.drawer_open span:before,
.drawer_open span:after {
  content: '';
  display: block;
  height: 3px;
  width: 25px;
  border-radius: 3px;
  background: #F0F0E0;
  transition: 0.5s;
  position: absolute;
}

/* 三本線の一番上の棒の位置調整 */
.drawer_open span:before {
  bottom: 8px;
}

/* 三本線の一番下の棒の位置調整 */
.drawer_open span:after {
  top: 8px;
}

/* アイコンがクリックされたら真ん中の線を透明にする */
#drawer_input:checked~.drawer_open span {
  background: #F0F0E0;
}

/* アイコンがクリックされたらアイコンが×印になように上下の線を回転 */
#drawer_input:checked~.drawer_open span::before {
  bottom: 0;
  transform: rotate(45deg);
}

#drawer_input:checked~.drawer_open span::after {
  top: 0;
  transform: rotate(-45deg);
}

/* メニューのデザイン*/
.nav_content {
  width: 100%;
  height: 100%;
  position: fixed;
  top: 0;
  left: 100%;
  /* メニューを画面の外に飛ばす */
  z-index: 99;
  background: #8DB2BA;
  transition: .5s;
}

/* メニュー黒ポチを消す */
.nav_list {
  list-style: none;
  padding: 50px;
}

a {
  color: #F0F0E0;
  font-size: 15pt;
  font-weight: bold;
  text-decoration: none;
}

/* アイコンがクリックされたらメニューを表示 */
#drawer_input:checked~.nav_content {
  left: 0;
  /* メニューを画面に入れる */
}
</style>

