<template>
  <div class="card">
    <div class="card-header row d-flex">
      <div class="col-3 col-md-6 col-lg-8 row px-0">
        <div class="col-12 col-lg-4 my-auto">
          <a
            href="#"
            class="btn btn-link link-underline link-underline-opacity-0 border rounded pt-2"
            :class="['link-' + auth.userColor.value ]"
            @click="$emit('close')"
          >
            <svg
              xmlns="http://www.w3.org/2000/svg"
              width="24"
              height="24"
              fill="currentColor"
              class="bi bi-caret-left"
              viewBox="0 0 16 16"
            >
              <path d="M10 12.796V3.204L4.519 8 10 12.796zm-.659.753-5.48-4.796a1 1 0 0 1 0-1.506l5.48-4.796A1 1 0 0 1 11 3.204v9.592a1 1 0 0 1-1.659.753z" />
            </svg>
            Vissza
          </a>
        </div>
        <div class="col-0 d-none col-lg-8 d-lg-inline my-auto truncate ms-0">
          <h2 class="">
            Előző rendelések
          </h2>
        </div>
      </div>
      <div class="col-9 col-md-6 col-lg-4 d-flex flex-fill px-0" />
    </div>
    <div class="row">
      <div class="col">
        <div class="">
          <HistoryDateStamp
            date-range="6"
            @selected-date="(date) => getHistroy(date)"
          />
        </div>
        <div class="row d-flex my-1">
          <div class="col text-center align-center">
            <span class="btn pe-none border border-secondary-subtle rounded">
              {{ basketSum }} Ft
            </span>
          </div>
          <div class="col text-center">
            <span class="btn pe-none border border-secondary-subtle rounded">
              {{ boxCount }} db doboz
            </span>
          </div>
          <div class="col text-center">
            <span class="btn pe-none border border-secondary-subtle rounded">
              {{ transportFeePerPerson }} Ft szállítás díj/fő
            </span>
          </div>
          <div class="col text-center">
            <span class="btn pe-none border border-secondary-subtle rounded">
              {{ personCount }} fő
            </span>
          </div>
        </div>
        <div
          v-for="(basket, personName) in history"
          :key="personName"
          class="row mt-1 mb-1"
        >
          <div class="list-group-item row m-0">
            <GlobalBasketPerson
              :name="personName"
              :person-basket="basket"
              :start-collapsed="true"
              :collapsable="true"
              :copyable="false"
            />
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import HistoryDateStamp from './HistoryDateStamp.vue'
import GlobalBasketPerson from './GlobalBasketPerson.vue'
import { useAuth } from '@/auth';
import { transportFeePerPerson, personCount, basketSum, boxCount } from '@/basket';

export default {
  name: 'FalusiHistroy',
  components: {
    HistoryDateStamp,
    GlobalBasketPerson
  },
  emits: ['close'],
  setup() {
    const auth = useAuth();
    return {
      auth,
      transportFeePerPerson,
      personCount,
      basketSum,
      boxCount
    }
  },
  data() {
    return {
      history: {}
    }
  },
  mounted() {
    this.getHistroy(new Date());
  },
  methods: {
    getHistroy: function(date) {
      let url = ''
      if (date === undefined) {
        url = `http://${window.location.host}/api/order/history`
      } else {
        url = `http://${window.location.host}/api/order/history/${new Date(date).toISOString().split('T')[0]}`
      }
      fetch(url)
        .then(response => response.json())
          .then(data => {
            this.history = data;
          })
        .catch(error => console.error(error));
    }
  }
}
</script>

<style>
</style>
