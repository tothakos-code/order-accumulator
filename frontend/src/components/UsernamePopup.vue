<template>
  <div v-if="isLoggedIn"  class="d-flex">
    <div class="btn-group">
      <button type="button" class="btn pe-none border border-secondary">{{ username }}</button>
      <button type="button" class="btn btn-outline-secondary dropdown-toggle dropdown-toggle-split" id="dropdownMenuButton1" data-bs-toggle="dropdown" aria-expanded="false" ></button>
      <ul class="dropdown-menu" aria-labelledby="dropdownMenuButton1">
        <li>
          <button class="dropdown-item" @click="showProfile = true">
            <span>
              Név szerkesztése
            </span>
            <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-pen" viewBox="0 0 16 16" data-darkreader-inline-fill="" style="--darkreader-inline-fill:currentColor;">
              <path d="m13.498.795.149-.149a1.207 1.207 0 1 1 1.707 1.708l-.149.148a1.5 1.5 0 0 1-.059 2.059L4.854 14.854a.5.5 0 0 1-.233.131l-4 1a.5.5 0 0 1-.606-.606l1-4a.5.5 0 0 1 .131-.232l9.642-9.642a.5.5 0 0 0-.642.056L6.854 4.854a.5.5 0 1 1-.708-.708L9.44.854A1.5 1.5 0 0 1 11.5.796a1.5 1.5 0 0 1 1.998-.001zm-.644.766a.5.5 0 0 0-.707 0L1.95 11.756l-.764 3.057 3.057-.764L14.44 3.854a.5.5 0 0 0 0-.708l-1.585-1.585z"></path>
            </svg>
          </button>
        </li>
        <li>
          <button class="dropdown-item" @click="this.$emit('toHistory')">
            <span>
              Előző rendelések
            </span>
            <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-clock-history" viewBox="0 0 16 16">
              <path d="M8.515 1.019A7 7 0 0 0 8 1V0a8 8 0 0 1 .589.022l-.074.997zm2.004.45a7.003 7.003 0 0 0-.985-.299l.219-.976c.383.086.76.2 1.126.342l-.36.933zm1.37.71a7.01 7.01 0 0 0-.439-.27l.493-.87a8.025 8.025 0 0 1 .979.654l-.615.789a6.996 6.996 0 0 0-.418-.302zm1.834 1.79a6.99 6.99 0 0 0-.653-.796l.724-.69c.27.285.52.59.747.91l-.818.576zm.744 1.352a7.08 7.08 0 0 0-.214-.468l.893-.45a7.976 7.976 0 0 1 .45 1.088l-.95.313a7.023 7.023 0 0 0-.179-.483zm.53 2.507a6.991 6.991 0 0 0-.1-1.025l.985-.17c.067.386.106.778.116 1.17l-1 .025zm-.131 1.538c.033-.17.06-.339.081-.51l.993.123a7.957 7.957 0 0 1-.23 1.155l-.964-.267c.046-.165.086-.332.12-.501zm-.952 2.379c.184-.29.346-.594.486-.908l.914.405c-.16.36-.345.706-.555 1.038l-.845-.535zm-.964 1.205c.122-.122.239-.248.35-.378l.758.653a8.073 8.073 0 0 1-.401.432l-.707-.707z"/>
              <path d="M8 1a7 7 0 1 0 4.95 11.95l.707.707A8.001 8.001 0 1 1 8 0v1z"/>
              <path d="M7.5 3a.5.5 0 0 1 .5.5v5.21l3.248 1.856a.5.5 0 0 1-.496.868l-3.5-2A.5.5 0 0 1 7 9V3.5a.5.5 0 0 1 .5-.5z"/>
            </svg>
          </button>
        </li>
      </ul>
    </div>
  </div>
  <div v-else class="">
    <button @click="showProfile = true" class="btn btn-dark">Bejelentkezés</button>
  </div>
  <Popup  :showModal="showProfile" title="Név választás" @cancel="showProfile = false" @confirm="this.saveUsername()">
    <p>Egy név ami alapján beazonosíthatnak téged.</p>
    <p>Nincs külön regisztráció. A név megadásával már létre is jön a fiókod.</p>
    <p>A fiókodba belépni későb a neved megadásával tudsz.</p>
    <div class="input-group mb-3">
      <span class="input-group-text">Név</span>
      <input type="text" v-model.trim="username" class="form-control" placeholder="Username" aria-label="Username" aria-describedby="basic-addon1">
    </div>
  </Popup>
</template>

<script>
import Popup from './Popup.vue';
import { useCookies } from "vue3-cookies";
import { state, socket } from "@/socket";

export default {
  name: 'UsernamePopup',
  components: {
    Popup
  },
  emits: ['toHistory'],
  setup() {
    const { cookies } = useCookies();
    return { cookies };
  },
  mounted() {
    if (this.$cookies.isKey('username')) {
      this.username = this.cookies.get('username');
      this.login();
    }

  },
  data() {
    return {
      showProfile: false,
      username: "",
      isLoggedIn: false
    }
  },
  methods: {
    saveUsername: function() {
      this.cookies.set("username", this.username, "365d");
      this.showProfile = false;
      this.login();
    },
    login: function() {
      socket.emit("User Login", {"username": this.username}, function(user) {
        state.user = user;
      });
      this.isLoggedIn= true;
    }
  }
}
</script>

<style>
</style>
