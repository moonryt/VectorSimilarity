<script setup lang="ts">

const embeddingFormula = String.raw`\text{文本}_1 \rightarrow \mathbf{a},\quad \text{文本}_2 \rightarrow \mathbf{b}`
const dotProductFormula = String.raw`\mathbf{a}\cdot\mathbf{b}=|\mathbf{a}||\mathbf{b}|\cos\theta`
const cosineFormula = String.raw`\cos\theta=\cos\langle\mathbf{a},\mathbf{b}\rangle=\frac{\mathbf{a}\cdot\mathbf{b}}{|\mathbf{a}|\cdot|\mathbf{b}|}`
const normalizedFormula = String.raw`n=\frac{\cos\theta+1}{2}`
const sigmoidFormula = String.raw`\sigma(n)=\frac{1}{1+e^{-8(n-0.65)}}`

</script>

<template>
  <n-card class="border-b-0!">
    <div class="space-y-5 leading-7 px-2">
      <p>
        要计算两段话的相似度，首先将两段话进行文本嵌入，得到分别代表两段话的词向量
        <n-equation class="inline-block align-middle" value="\mathbf{a}" :inline="true" />
        和
        <n-equation class="inline-block align-middle" value="\mathbf{b}" :inline="true" />
        。
      </p>

      <div class="flex justify-center">
        <n-equation :value="embeddingFormula" />
      </div>

      <p>
        设两向量夹角为
        <n-equation class="inline-block align-middle" value="\theta" :inline="true" />。
        计算相似度的原理，是利用高中学过的点乘定义式：
      </p>

      <div class="flex justify-center">
        <n-equation :value="dotProductFormula" />
      </div>

      <p>
        易知
        <n-equation class="inline-block align-middle" value="\cos\theta" :inline="true" />
        为两向量的夹角余弦值。因为
        <n-equation class="inline-block align-middle" value="\cos x" :inline="true" />
        在
        <n-equation class="inline-block align-middle" value="[0,\pi]" :inline="true" />
        上单调递减，夹角越大函数值越小，这就是为什么
        <n-equation class="inline-block align-middle" value="\cos\theta" :inline="true" />
        能代表两个向量相似度的原因。「语义相似度」就是该余弦值百分数化的结果。
      </p>

      <div class="flex justify-center">
        <n-equation :value="cosineFormula" />
      </div>

      <p>
        但是实践测试中，余弦值均值大约集中在
        <n-equation class="inline-block align-middle" value="0.4\sim0.6" :inline="true" />
        ，直接展示会让结果比较机器化，心理上的激励也更小，所以需要对中间区间进行非线性变换调整。
      </p>

      <p>
        S 形函数（Sigmoid function）就十分适合这个工作。我们先利用
        <n-equation class="inline-block align-middle" value="\frac{\cos\theta+1}{2}" :inline="true" />
        将余弦函数值域映射为
        <n-equation class="inline-block align-middle" value="[0,1]" :inline="true" />
        ：
      </p>

      <div class="flex justify-center">
        <n-equation :value="normalizedFormula" />
      </div>

      <p>
        再利用 S 函数对结果进行调整：
      </p>

      <div class="flex justify-center">
        <n-equation :value="sigmoidFormula" />
      </div>

      <p>
        准确来讲，该函数会让中间区间的变化更加敏感，而两端逐渐趋于饱和，使结果更加符合心理预期，这就是两词语间的「近似度」。
      </p>
      <p>
        综上，这几个函数是对本站算法的集中体现，所以其实对比页那个加载公式动画，计算虽为假，但算法却为真。
      </p>
    </div>
  </n-card>

</template>

<style scoped>

</style>
