<script>

export default {
  props: ['width', 'user'],
  data() {
    return {
      imageWidth: this.width || 80,
    }
  }
}

</script>

<template>
  <img
    v-if="user.isJeff"
    class="rounded-circle"
    :width="imageWidth"
    src="@/assets/jeff.png" alt="" />

  <div
    v-else
    class="
      d-flex flex-column justify-content-center align-items-center
      border rounded-circle
      bg-danger-subtle
    "
    :style="{'width': imageWidth + 'px', 'height': imageWidth + 'px'}"
  >
    <i class="bi bi-person" :style="{'font-size': (imageWidth / 2) + 'px'}"></i>
  </div>
</template>
