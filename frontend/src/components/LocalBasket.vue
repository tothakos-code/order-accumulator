<template>
  <div class="card">
    <div class="card-header row d-flex align-items-center">
      <div class="col-4">
        <h2>Kosarad</h2>
      </div>
      <div class="col-4 align-items-center">
        <span>{{ sumBasket }} Ft + Szállítási díj</span>
      </div>
      <div class="col-4 text-end">
        <button class="btn btn-warning" @click="this.clearBasket()">Kosarad ürítése
          <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" fill="currentColor" class="bi bi-cart-x" viewBox="0 0 16 16">
            <path d="M7.354 5.646a.5.5 0 1 0-.708.708L7.793 7.5 6.646 8.646a.5.5 0 1 0 .708.708L8.5 8.207l1.146 1.147a.5.5 0 0 0 .708-.708L9.207 7.5l1.147-1.146a.5.5 0 0 0-.708-.708L8.5 6.793 7.354 5.646z"/>
            <path d="M.5 1a.5.5 0 0 0 0 1h1.11l.401 1.607 1.498 7.985A.5.5 0 0 0 4 12h1a2 2 0 1 0 0 4 2 2 0 0 0 0-4h7a2 2 0 1 0 0 4 2 2 0 0 0 0-4h1a.5.5 0 0 0 .491-.408l1.5-8A.5.5 0 0 0 14.5 3H2.89l-.405-1.621A.5.5 0 0 0 2 1H.5zm3.915 10L3.102 4h10.796l-1.313 7h-8.17zM6 14a1 1 0 1 1-2 0 1 1 0 0 1 2 0zm7 0a1 1 0 1 1-2 0 1 1 0 0 1 2 0z"/>
          </svg>
        </button>
      </div>
    </div>
    <div class="row">
      <div class="list-group pe-0">
        <div v-for="(item, itemSizeKey) in basket" :key="itemSizeKey" class="list-group-item d-flex justify-content-between">
          <div class="col-2">
            <span class="badge bg-warning-subtle border border-warning-subtle text-warning-emphasis rounded-pill">{{  item.quantity }} x</span>
          </div>
          <div class="col-8">
            <span>{{ item.name }} ({{item.size}}) - {{item.price}}</span>
          </div>
          <div class="col-2 text-end">
            <button @click="this.deleteFromBasket(itemSizeKey, item)" type="button" title="Törlés" class="btn btn-close"></button>
          </div>
        </div>
        <div v-if="isBasketEmpty" class="list-group-item d-flex justify-content-center">
          <div class="">
            <span>
              Üres a kosarad
            </span>
            <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" fill="currentColor" class="bi bi-cart-x" viewBox="0 0 16 16">
              <path d="M7.354 5.646a.5.5 0 1 0-.708.708L7.793 7.5 6.646 8.646a.5.5 0 1 0 .708.708L8.5 8.207l1.146 1.147a.5.5 0 0 0 .708-.708L9.207 7.5l1.147-1.146a.5.5 0 0 0-.708-.708L8.5 6.793 7.354 5.646z"/>
              <path d="M.5 1a.5.5 0 0 0 0 1h1.11l.401 1.607 1.498 7.985A.5.5 0 0 0 4 12h1a2 2 0 1 0 0 4 2 2 0 0 0 0-4h7a2 2 0 1 0 0 4 2 2 0 0 0 0-4h1a.5.5 0 0 0 .491-.408l1.5-8A.5.5 0 0 0 14.5 3H2.89l-.405-1.621A.5.5 0 0 0 2 1H.5zm3.915 10L3.102 4h10.796l-1.313 7h-8.17zM6 14a1 1 0 1 1-2 0 1 1 0 0 1 2 0zm7 0a1 1 0 1 1-2 0 1 1 0 0 1 2 0z"/>
            </svg>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { useCookies } from "vue3-cookies";
import { state } from "@/socket";

export default {
  name: 'LocalBasket',
  setup() {
    const { cookies } = useCookies();
    return { cookies };
  },
  emits: ['basketUpdate'],
  data() {
    return {
      basket: {}
    };
  },
  mounted() {
    this.updateBasket();
  },
  methods: {
    deleteFromBasket: function(itemSizeKey, basketItem) {
      if ( state.orderState === 'order') {
        alert("Figyelem! A rendelő elkezdte áthelyezni a falusiba a kosarat és lehet, hogy nem veszi észre, hogy te változtattál a kosaradon. Jelezd neki mielött nem késő!")
      }
      if ( state.orderState === 'closed') {
        alert("A rendelés már el lett küldve. Már nem módosíthatod a kosaradat.")
        return;
      }
      if (basketItem.quantity == 1) {
        // Otherwise, remove the entry from the basket
        delete this.basket[itemSizeKey];
      } else {
        // If the item exists in the basket, decrement the quantity
        basketItem.quantity -= 1;
      }
      this.cookies.set('basket', this.basket, '16h');
      this.$emit('basketUpdate');
    },
    updateBasket: function() {
      this.basket = JSON.parse(
        JSON.stringify(
          this.cookies.get('basket')
        )
      ) || {};
    },
    clearBasket: function() {
      if ( state.orderState === 'order') {
        alert("Figyelem! A rendelő elkezdte áthelyezni a falusiba a kosarat és lehet, hogy nem veszi észre, hogy te változtattál a kosaradon. Jelezd neki mielött nem késő!")
      }
      if ( state.orderState === 'closed') {
        alert("A rendelés már el lett küldve. Már nem módosíthatod a kosaradat.")
        return;
      }
      // Remove the basket cookie
      this.cookies.set('basket', {}, '16h');
      this.$emit('basketUpdate');
    }
  },
  computed: {
    isBasketEmpty() {
      return Object.keys(this.basket).length == 0;
    },
    sumBasket() {
      let sum = 0;
      Object.values(this.basket).forEach(item => {
        sum+= Number(item.quantity) * Number((item.price).split(' ')[0]);
      });
      return sum;
    }
  }
}
</script>

<style>
</style>
