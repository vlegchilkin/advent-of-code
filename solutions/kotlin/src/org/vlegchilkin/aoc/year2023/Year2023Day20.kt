package org.vlegchilkin.aoc.year2023

import org.vlegchilkin.aoc.*


/**
 * 2023/20: Pulse Propagation
 */
class Year2023Day20(input: String) : Solution {
  data class Module(val type: Char?, val outputs: List<String>)

  private val modules = input.toList {
    val (a, b) = it.split(" -> ")
    val (name, type) = if (a[0].isLetter()) a to null else a.substring(1) to a[0]
    val outputs = b.split(", ")
    name to Module(type, outputs)
  }.toMap()

  override fun partAB(): Pair<Any, Any> {
    val inputs = modules.flatMap { (k, v) -> v.outputs.map { it to k } }.groupBy({ it.first }, { it.second })
    val states = inputs.map { (k, v) -> k to IntArray(v.size) }.toMap().toMutableMap()
    val (counter, clicksLimitForCounter) = mutableListOf(0, 0) to 1000
    val (cyclicModule, cycles) = "ls" to mutableMapOf<Int, Int>()

    fun single(click: Int) {
      val queue = ArrayDeque(listOf(("button" to "broadcaster") to 0))
      while (queue.isNotEmpty()) {
        val (wire, signal) = queue.removeFirst()
        val (inMod, outMod) = wire
        if (click <= clicksLimitForCounter) counter[signal] += 1

        val module = modules[outMod] ?: continue
        val outSignal = when (module.type) {
          '%' -> if (signal == 1) null else states[outMod]!!.apply { this[0] = 1 - this[0] }[0]
          '&' -> {
            val state = states[outMod]!!.apply {
              val pin = inputs[outMod]!!.indexOfFirst { it == inMod }
              this[pin] = signal
            }
            if (state.all { it == 1 }) 0 else 1
          }
          else -> signal
        }

        outSignal?.let { sig ->
          module.outputs.forEach { queue.addLast((outMod to it) to sig) }
        }

        if (outMod == cyclicModule) {
          states[cyclicModule]!!.forEachIndexed { i, value ->
            if (value == 1) cycles.putIfAbsent(i, click)
          }
        }
      }
    }

    var click = 0
    val requiredCycles = inputs[cyclicModule]!!.size
    while (click < clicksLimitForCounter || cycles.size < requiredCycles) {
      single(++click)
    }

    return counter[0] * counter[1] to cycles.values.lcm()
  }

  companion object : Test(2023, 20, { Year2023Day20(it) })
}
