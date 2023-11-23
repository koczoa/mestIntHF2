import kotlin.math.log2
import java.io.File

fun main() {
    println("asdf")

    var asdf = File("train.csv").readLines().map{it.split(",").map{it.toInt()}}
    //print(asdf)
    var fs = asdf.map{it.dropLast(1)}
    var ls = asdf.map{it.last()}
    var tree = rec(fs, ls)
    var testFs = File("test.csv").readLines().map{it.split(",").map{it.toInt()}}

    var res = File("results.csv")
    for (h in testFs) {
        res.appendText(tree.traverse(h).toString())
        res.appendText("\n")
    }
}

class node(val sep: Pair<Int, Int>?, val left: node?, val right: node?, val label: Int?) {
    override fun toString() : String {
        if(label != null) {
            return label.toString()
        } else {
            return "(" + left.toString() + right.toString() + ")"
        }
    }
    fun traverse(haus : List<Int>) :Int {
        if(label != null) {
            return label
        } else {
            if(haus[sep!!.first] <= sep.second) {
                return left!!.traverse(haus)
            } else {
                return right!!.traverse(haus)
            }
        }
    }
}

fun rec(features: List<List<Int>>, labels: List<Int>) :node {
    val myFeatures = features.zip(labels)
    var best_sep = get_best_separation(features, labels)
    var left = myFeatures.filter { (it.first[best_sep.first] <= best_sep.second) }
    var right = myFeatures.filter { (it.first[best_sep.first] > best_sep.second) }
    if(left.size == 0 || right.size == 0) {
        return node(null, null, null, labels[0])
    }
    return node(best_sep, rec(left.map{it.first}, left.map{it.second}), rec(right.map{it.first}, right.map{it.second}), null)
}

fun get_entropy(n_cat1 : Int, n_cat2: Int) : Float {
    if(n_cat1 == 0 || n_cat2 == 0) {
        return 0f
    }
    val p1 = n_cat1.toFloat() / (n_cat1 + n_cat2).toFloat()
    val p2 = n_cat2.toFloat() / (n_cat1 + n_cat2).toFloat()
    return - ((p1 * log2(p1)) + (p2 * log2(p2)))
}

fun get_best_separation(features: List<List<Int>>, labels: List<Int>) : Pair<Int, Int> {
    var best_separation_feature = 0
    var best_separation_value = 0
    val myFeatures = features.zip(labels)
    val numberOfOnes = labels.count { it == 1 }
    var start_entropy = get_entropy(numberOfOnes, labels.count() - numberOfOnes)
    var best_informationGain = -1f
    for (feature in myFeatures) {
        for(f in feature.first.withIndex()) {
            var smol = myFeatures.filter { (it.first[f.index] <= f.value) }
            var bigg = myFeatures.filter { (it.first[f.index] > f.value) }
            var smolEntropy = get_entropy(smol.count { it.second == 1}, smol.count { it.second == 0})
            var biggEntropy = get_entropy(bigg.count { it.second == 1}, bigg.count { it.second == 0})
            var thisInfoGain = start_entropy - ((smol.size.toFloat() * smolEntropy.toFloat() + bigg.size.toFloat() * biggEntropy.toFloat()) / myFeatures.size.toFloat())

            if(thisInfoGain > best_informationGain) {
                best_informationGain = thisInfoGain
                best_separation_value = f.value
                best_separation_feature = f.index
            }
        }
    }
    return best_separation_feature to best_separation_value
}