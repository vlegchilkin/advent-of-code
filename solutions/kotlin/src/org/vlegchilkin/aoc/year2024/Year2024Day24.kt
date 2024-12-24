package org.vlegchilkin.aoc.year2024

import org.vlegchilkin.aoc.*

enum class Logic(val op: (Int, Int) -> Int) { AND(Int::and), XOR(Int::xor), OR(Int::or) }

data class Element(val logic: Logic, val in1: String, val in2: String, val out: String)

/**
 * 2024/24: Crossed Wires
 */
class Year2024Day24(input: String) : Solution {
  private val initStates: Map<String, Int>
  private val elements: List<Element>

  init {
    val (initStates, instructions) = input.toList("\n\n") { block -> block.toList { it } }
    this.initStates = initStates.associate { it.substringBefore(':') to it.substringAfter(' ').toInt() }
    this.elements = instructions.map { line ->
      val (in1, logic, in2, _, out) = line.split(' ')
      Element(Logic.valueOf(logic), in1, in2, out)
    }
  }

  override fun partA(): Long {
    val outputs = elements.associateBy { it.out }
    val states = initStates.toMutableMap()
    fun dfs(pin: String): Int {
      states[pin]?.let { return it }
      val instruction = outputs[pin] ?: error("No output for $pin")
      val out = with(instruction) {
        val a = dfs(in1)
        val b = dfs(in2)
        logic.op(a, b)
      }
      return out.also { states[pin] = it }
    }

    val zPins = outputs.keys.filter { it.startsWith('z') }.sortedDescending()
    val result = zPins.fold(0L) { res, pin ->
      (res shl 1) + dfs(pin)
    }
    return result
  }

  /**
   * N - number of output pins
   * X,Y - input
   * Z - output
   * R - carry on flag
   *
   * Xi -----v
   *         AND -> Fi ------------------+
   *         XOR -> Wi --v                \
   * Yi -----^           XOR -> (Zi)      OR -> (Ri)
   *                     AND -> Vi -------^
   * R(i-1)  ------------^
   *
   *
   * R0 = X0 AND Y0
   * Z0 = X0 XOR Y0
   * for i>0:
   *   Fi = Xi AND Yi for i>=1,
   *   Wi = Xi XOR Yi for i>=1
   *   Vi = Wi AND R(i-1)
   *   Zi = Wi XOR R(i-1)
   *   Ri = Fi OR Vi
   *
   */
  override fun partB(): Any {
    val outputs = elements.associateBy { it.out }
    fun pin(c: Char, idx: Int) = "$c${idx.toString().padStart(2, '0')}"
    val n = outputs.keys.filter { it.startsWith('z') }.max().substring(1).toInt()
    val f = mutableMapOf<Int, Element>()
    val w = mutableMapOf<Int, Element>()
    val v = mutableMapOf<Int, Element>()
    val r = mutableMapOf<Int, Element>()
    val z = mutableMapOf<Int, Element>()
    val crosses = elements.flatMap { listOf(it.in1, it.in2, it.out) }.associateWith { it }.toMutableMap()

    fun find(inp: Pair<String, String>): List<Element> {
      val (x1, x2) = crosses.getValue(inp.first) to crosses.getValue(inp.second)
      return elements.filter { instr ->
        with(instr) { (in1 == x1 && in2 == x2) || (in1 == x2 && in2 == x1) }
      }
    }

    // init F, W, R[0] and Z[0] because they are based on input pins
    for (i in 0..<n) {
      val (x, y) = pin('x', i) to pin('y', i)
      for (instr in find(x to y)) {
        when (instr.logic) {
          Logic.AND -> if (i > 0) f[i] = instr else r[0] = instr
          Logic.XOR -> if (i > 0) w[i] = instr else z[0] = instr
          Logic.OR -> error("Can't be OR")
        }
      }
    }

    // fill V, R, Z
    for (i in 1..<n) {
      val fi = checkNotNull(f[i]).out
      val wi = checkNotNull(w[i]).out
      val ri1 = checkNotNull(r[i - 1]).out
      val possible = find(wi to ri1).takeIf { it.isNotEmpty() } ?: run { // Fi crossed with Wi
        crosses[fi] = wi
        crosses[wi] = fi
        find(wi to ri1)
      }
      for (instr in possible) {
        when (instr.logic) {
          Logic.AND -> v[i] = instr
          Logic.XOR -> {
            z[i] = instr
            val havePin = instr.out
            val needPin = pin('z', i)
            if (havePin != needPin) { // Z pin missmatch, make a cross
              crosses[havePin] = needPin
              crosses[needPin] = havePin
            }
          }
          Logic.OR -> error("Can't be OR")
        }
      }

      checkNotNull(z[i])
      val vi = checkNotNull(v[i]).out
      for (instr in find(fi to vi)) {
        when (instr.logic) {
          Logic.OR -> r[i] = instr
          else -> error("Can't be AND / XOR")
        }
      }
    }
    val result = crosses.entries.filter { it.key != it.value }.map { it.key }.sorted()
    return result.joinToString(",")
  }

  companion object : Test(2024, 24, { Year2024Day24(it) })
}
