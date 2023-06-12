<script>

export default {
  props: ['user'],
}

</script>

<template>
  <p
    class="d-inline text-center m-0 p-0"
    :class="{'text-danger': user.isPrivate}"
  >{{ user.userFullName }} <span v-if="user.isPrivate" class="fw-bold">(private)</span></p>
</template>
