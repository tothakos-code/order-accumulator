<template>
  <div class="list-group-item row d-flex ">
    <div class="col-12 col-lg-8 p-0">
      <span>
        {{ item.label }}
      </span>
    </div>
    <div class="col-12 col-lg-4 p-0 flex-wrap">
      <div class="d-flex justify-content-end">
        <span
          v-if="item.sold_out"
          class="btn pe-none btn-outline-danger btn-sm"
        >Elfogyott</span>
        <button
          v-for="size in item.sizes"
          v-else
          :key="item.id+'-'+size.size"
          class="btn btn-sm col-6 col-sm-6 ms-2"
          :class="['btn-' + auth.userColor.value ]"
          @click="addToBasket(item.id, size.size)"
        >
          <span class="text-nowrap me-1">{{ size.size }}</span>
          <span class="text-nowrap">{{ size.price }}</span>
        </button>
      </div>
    </div>
  </div>
</template>

<script>
import { state, socket } from "@/socket";
import { useAuth } from "@/auth";
import { notify } from "@kyvg/vue3-notification";

export default {
  name: 'FalusiMenu',
  props: {
    'item':{
      type: Object,
      default: new Object()
    },
  },
  setup() {
    const auth = useAuth();
    return {
      auth
    }
  },
  computed: {
    currentUserState() {
      return state.userStates[state.user.username];
    }
  },
  methods: {
    addToBasket: function(fid, size) {
      if (!this.auth.isLoggedIn.value) {
        notify({
          type: "warn",
          text: "Jelentkezz be a rendeléshez!",
        });
        return;
      }
      if (state.orderState === 'closed') {
        notify({
          type: "warn",
          text: "A rendelés már el lett küldve. Már nem módosíthatod a kosaradat.",
        });
        return;
      }
      if (this.currentUserState === 'skip') {
        socket.emit("User Daily State Change",{ 'id': state.user.id, 'new_state':'none' });
      }
      const itemSizeKey = fid + '-' + size;
      const updated_basket = structuredClone(state.localBasket);
      if (updated_basket[itemSizeKey]) {
        // If the item already exists in the basket, increment the quantity
        updated_basket[itemSizeKey].quantity += 1;
      } else {
        // Otherwise, add a new entry to the basket
        updated_basket[itemSizeKey] = {
          id: fid,
          size: size,
          quantity: 1
        };
      }
      socket.emit("Server Basket Update", { "userid": state.user.id, "basket": updated_basket, "order_date": state.selectedDate.toISOString().split('T')[0] });

    }
  }
}
</script>

<style>
</style>
