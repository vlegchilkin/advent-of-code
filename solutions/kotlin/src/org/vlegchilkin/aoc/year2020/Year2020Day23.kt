package org.vlegchilkin.aoc.year2020

import org.vlegchilkin.aoc.Solution
import org.vlegchilkin.aoc.Test


class CircleList<T>(initState: Collection<T>) {
  var current: Node<T>
  val index: Map<T, Node<T>>

  init {
    var head: Node<T>? = null
    val it = initState.iterator()
    var tmp: Node<T>? = null
    while (it.hasNext()) {
      val value = it.next()
      val next = Node(value, null)
      if (tmp == null) head = next else tmp.next = next
      tmp = next
    }
    current = head!!
    tmp!!.next = current

    index = mutableMapOf()
    var swp = current.next!!
    while (swp != current) {
      index[swp.item] = swp
      swp = swp.next!!
    }
    index[current.item] = current
  }

  class Node<T>(var item: T, var next: Node<T>?)

  fun asSequence(offset: Node<T>? = null) = sequence {
    val start = offset ?: current
    var tmp = start.next!!
    yield(start.item)
    while (start != tmp) {
      yield(tmp.item)
      tmp = tmp.next!!
    }
  }

  fun cutChain(size: Int): Pair<Node<T>, Node<T>> {
    val head = current.next!!
    var tail = head
    repeat(size - 1) { tail = tail.next!! }
    current.next = tail.next!!
    tail.next = null
    return head to tail
  }

  fun insertChain(chain: Pair<Node<T>, Node<T>>, insertAfter: Node<T>) {
    val tail = insertAfter.next!!
    insertAfter.next = chain.first
    chain.second.next = tail
  }

  fun next() {
    current = current.next!!
  }

  override fun toString(): String {
    return asSequence().joinToString(",")
  }
}

infix fun <T> Pair<CircleList.Node<T>, CircleList.Node<T>>.contains(value: T): Boolean {
  var tmp: CircleList.Node<T>? = this.first
  while (tmp != null) {
    if (tmp.item == value) return true
    tmp = tmp.next
  }
  return false
}

class Year2020Day23(input: String) : Solution {
  private val state = input.trim().map { it - '0' }
  private fun simulate(maxValue: Int, rounds: Int): CircleList<Int> {
    val buffer = CircleList(state + (10..maxValue))

    fun round() {
      val chain = buffer.cutChain(3)
      var goal = buffer.current.item
      do {
        goal = if (goal > 1) goal - 1 else maxValue
      }
      while (chain contains goal)
      buffer.insertChain(chain, buffer.index[goal]!!)
      buffer.next()
    }

    repeat(rounds) {
      round()
    }
    return buffer
  }

  override fun partA(): Long {
    val buffer = simulate(9, 100)
    return buffer.asSequence(buffer.index[1]).drop(1).fold(0L) { acc, v -> acc * 10 + v }
  }

  override fun partB(): Long {
    val buffer = simulate(1_000_000, 10_000_000)
    val nodeOne = buffer.index[1]
    return 1L * nodeOne!!.next!!.item * nodeOne.next!!.next!!.item
  }

  companion object : Test(2020, 23, { Year2020Day23(it) })
}