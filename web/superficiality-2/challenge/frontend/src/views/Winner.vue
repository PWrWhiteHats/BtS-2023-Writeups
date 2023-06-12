<script>

export default {
  computed: {
    winnerFlag() {
      return this.$route.params.winnerFlag;
    }
  }
}

</script>

<template>

  <div class="fs-1 text-center p-5">
    <p>Winner winner chicken dinner!</p>
    <p class="text-danger">Prize flag: {{ winnerFlag }}</p>
  </div>

</template>
