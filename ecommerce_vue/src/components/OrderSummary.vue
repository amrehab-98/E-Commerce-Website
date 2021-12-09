<template>
    <div class="box mb-4">

        <table class="table is-fullwidth">
            <thead>
                <tr>
                    <th width="25%">Product</th>
                    <th width="25%">Price</th>
                    <th width="25%">Quantity</th>
                    <th width="25%">Total</th>
                </tr>
            </thead>

            <tbody>
                <tr
                    v-for="item in order.items"
                    v-bind:key="item.product.id"
                >
                    <td width="25%">{{ item.product.name }}</td>
                    <td width="25%">${{ item.product.price }}</td>
                    <td width="25%">{{ item.quantity }}</td>
                    <td width="25%">${{ getItemTotal(item).toFixed(2) }}</td>
                </tr>
            </tbody>
        </table>
    </div>
</template>

<script>
export default {
    name: 'OrderSummary',
    props: {
        order: Object
    },
    methods: {
        getItemTotal(item) {
            return item.quantity * item.product.price
        },
        orderTotalLength(order) {
            return order.items.reduce((acc, curVal) => {
                return acc += curVal.quantity
            }, 0)
        },
    }
}
</script>