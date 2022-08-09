from funlib.learn.torch.losses import ultrametric_loss

import numpy as np
import torch
import pytest


def test_zero():

    embedding = np.zeros((1, 3, 10, 10, 10), dtype=np.float32)
    segmentation = np.ones((1, 1, 10, 10, 10), dtype=np.int64)

    embedding = torch.from_numpy(embedding).float()
    segmentation = torch.from_numpy(segmentation)

    loss, emst, edges_u, edges_v, distances, *_ = ultrametric_loss(
        embedding, segmentation, add_coordinates=False,
    )

    assert pytest.approx(float(loss)) == 0
    assert pytest.approx(np.sum(distances.numpy())) == 0


def test_zero_with_coordinates():

    embedding = np.zeros((1, 3, 10, 10, 10), dtype=np.float32)
    segmentation = np.ones((1, 1, 10, 10, 10), dtype=np.int64)

    embedding = torch.from_numpy(embedding).float()
    segmentation = torch.from_numpy(segmentation)

    loss, emst, edges_u, edges_v, distances, *_ = ultrametric_loss(
        embedding, segmentation, add_coordinates=True,
    )

    assert pytest.approx(float(loss)) == 1
    assert pytest.approx(np.sum(distances.numpy())) == 999


def test_simple():

    embedding = np.array([[[[0, 1, 2], [3, 4, 5], [6, 7, 8]]]], dtype=np.float32)

    segmentation = np.array([[[[1, 1, 1], [2, 2, 2], [3, 3, 3]]]], dtype=np.int64)

    # number of positive pairs: 3*3 = 9
    # number of negative pairs: 3*3*3 = 27
    # total number of pairs: 9*8/2 = 36

    # loss on positive pairs: 9*1 = 9
    # loss on negative pairs: 27*1 = 27
    # total loss = 36
    # total loss per edge = 1

    embedding = torch.from_numpy(embedding).float()
    segmentation = torch.from_numpy(segmentation)

    loss, emst, edges_u, edges_v, distances, *_ = ultrametric_loss(
        embedding, segmentation, alpha=2, add_coordinates=False, balance=False,
    )

    assert pytest.approx(float(loss)) == 1.0
    assert pytest.approx(np.sum(distances.numpy())) == 8

    loss, emst, edges_u, edges_v, distances, *_ = ultrametric_loss(
        embedding, segmentation, alpha=2, add_coordinates=False,
    )

    assert pytest.approx(float(loss)) == 2.0
    assert pytest.approx(np.sum(distances.numpy())) == 8


def test_background():

    embedding = np.array([[[[0, 1, 2], [4, 5, 6], [8, 9, 10]]]], dtype=np.float32)

    segmentation = np.array([[[[1, 1, 1], [0, 0, 0], [3, 3, 3]]]], dtype=np.int64)

    # number of positive pairs: 2*3 = 6
    # number of negative pairs: 3*3*3 = 27
    # number of background pairs: 3
    # total number of pairs (without background pairs): 33

    # loss on positive pairs: 6*1 = 6
    # loss on negative pairs: 27*2^2 = 108
    # total loss = 114
    # total loss per pair = 3.455
    # total loss per pos pair = 1
    # total loss per neg pair = 4

    embedding = torch.from_numpy(embedding).float()
    segmentation = torch.from_numpy(segmentation)

    loss, emst, edges_u, edges_v, distances, *_ = ultrametric_loss(
        embedding, segmentation, alpha=4, add_coordinates=False, balance=False,
    )

    assert pytest.approx(float(loss), 1e-3) == 3.4545
    assert pytest.approx(np.sum(distances.numpy()),) == 10


def test_mask():

    embedding = np.array([[[[0, 1, 2], [3, 4, 5], [6, 7, 8]]]], dtype=np.float32)

    segmentation = np.array([[[[1, 1, 1], [2, 2, 2], [3, 3, 3]]]], dtype=np.int64)

    embedding = torch.from_numpy(embedding).float()
    segmentation = torch.from_numpy(segmentation)

    # empty mask

    mask = np.zeros((1, 1, 3, 3), dtype=np.bool)
    mask = torch.from_numpy(mask)

    loss, emst, edges_u, edges_v, distances, *_ = ultrametric_loss(
        embedding, segmentation, mask=mask, alpha=2, add_coordinates=False,
    )

    assert pytest.approx(float(loss)) == 0.0
    assert pytest.approx(np.sum(distances.numpy())) == 0

    # mask with only one point

    mask = np.zeros((1, 1, 3, 3), dtype=np.bool)
    mask[0, 0, 1, 1] = True
    mask = torch.from_numpy(mask)

    loss, emst, edges_u, edges_v, distances, *_ = ultrametric_loss(
        embedding, segmentation, mask=mask, alpha=2, add_coordinates=False,
    )

    assert pytest.approx(float(loss)) == 0.0
    assert pytest.approx(np.sum(distances.numpy())) == 0

    # mask with two points

    mask = np.zeros((1, 1, 3, 3), dtype=np.bool)
    mask[0, 0, 1, 1] = True
    mask[0, 0, 0, 0] = True
    mask = torch.from_numpy(mask)

    loss, emst, edges_u, edges_v, distances, *_ = ultrametric_loss(
        embedding, segmentation, mask=mask, alpha=5, add_coordinates=False,
    )

    assert pytest.approx(float(loss)) == 1.0
    assert pytest.approx(np.sum(distances.numpy())) == 4.0


def test_constrained_mask():

    embedding = np.array([[[[0, 1, 2], [3, 4, 5], [6, 7, 8]]]], dtype=np.float32)

    segmentation = np.array([[[[1, 1, 1], [2, 2, 2], [3, 3, 3]]]], dtype=np.int64)

    embedding = torch.from_numpy(embedding).float()
    segmentation = torch.from_numpy(segmentation)

    # empty mask

    mask = np.zeros((1, 1, 3, 3), dtype=np.bool)
    mask = torch.from_numpy(mask)

    loss, emst, edges_u, edges_v, distances, *_ = ultrametric_loss(
        embedding,
        segmentation,
        mask=mask,
        constrained_emst=True,
        alpha=2,
        add_coordinates=False,
    )

    assert pytest.approx(float(loss)) == 0.0
    assert pytest.approx(np.sum(distances.numpy())) == 0

    # mask with only one point

    mask = np.zeros((1, 1, 3, 3), dtype=np.bool)
    mask[0, 0, 1, 1] = True
    mask = torch.from_numpy(mask)

    loss, emst, edges_u, edges_v, distances, *_ = ultrametric_loss(
        embedding,
        segmentation,
        mask=mask,
        constrained_emst=True,
        alpha=2,
        add_coordinates=False,
    )

    assert pytest.approx(float(loss)) == 0.0
    assert pytest.approx(np.sum(distances.numpy())) == 0

    # mask with two points

    mask = np.zeros((1, 1, 3, 3), dtype=np.bool)
    mask[0, 0, 1, 1] = True
    mask[0, 0, 0, 0] = True
    mask = torch.from_numpy(mask)

    loss, emst, edges_u, edges_v, distances, *_ = ultrametric_loss(
        embedding,
        segmentation,
        mask=mask,
        constrained_emst=True,
        alpha=5,
        add_coordinates=False,
    )

    assert pytest.approx(float(loss)) == 1.0
    assert pytest.approx(np.sum(distances.numpy())) == 4.0


def test_constrained():

    embedding = np.array([[[[0, 1, 101], [2, 3, 4], [5, 6, 7]]]], dtype=np.float32)

    segmentation = np.array([[[[1, 1, 1], [2, 2, 2], [3, 3, 3]]]], dtype=np.int64)

    # number of positive pairs: 3*3 = 9
    # number of negative pairs: 3*3*3 = 27
    # total number of pairs: 9*8/2 = 36

    # loss on positive pairs: 6*1 + 1 + 2*100^2 = 20007
    # loss on negative pairs: 27*1 = 27
    # total loss: 1/9*20007 + 1/27*27 = 2224

    embedding = torch.from_numpy(embedding).float()
    segmentation = torch.from_numpy(segmentation)

    loss, emst, edges_u, edges_v, distances, *_ = ultrametric_loss(
        embedding, segmentation, alpha=2, add_coordinates=False, constrained_emst=True,
    )

    assert pytest.approx(float(loss)) == 2224
    assert pytest.approx(np.sum(distances.numpy())) == 107


def test_ambiguous_unkown():

    embedding = np.array([[[[0, 1]]]], dtype=np.float32)

    segmentation = np.array([[[[-1, 0]]]], dtype=np.int64)

    # number of positive pairs: 0
    # number of negative pairs: 1
    # total number of pairs: 0

    # loss on positive pairs: 0
    # loss on negative pairs: 1
    # total loss: 1

    embedding = torch.from_numpy(embedding).float()
    segmentation = torch.from_numpy(segmentation)

    loss, emst, edges_u, edges_v, distances, *_ = ultrametric_loss(
        embedding,
        segmentation,
        alpha=2,
        balance=True,
        add_coordinates=False,
        constrained_emst=True,
    )

    assert pytest.approx(float(loss)) == 1
    assert pytest.approx(np.sum(distances.numpy())) == 1

    embedding = np.array([[[[0, 1]]]], dtype=np.float32)

    segmentation = np.array([[[[0, -1]]]], dtype=np.int64)

    # number of positive pairs: 0
    # number of negative pairs: 1
    # total number of pairs: 0

    # loss on positive pairs: 0
    # loss on negative pairs: 1
    # total loss: 1

    embedding = torch.from_numpy(embedding).float()
    segmentation = torch.from_numpy(segmentation)

    loss, emst, edges_u, edges_v, distances, *_ = ultrametric_loss(
        embedding,
        segmentation,
        alpha=2,
        balance=True,
        add_coordinates=False,
        constrained_emst=True,
    )

    assert pytest.approx(float(loss)) == 1
    assert pytest.approx(np.sum(distances.numpy())) == 1


def test_ambiguous_known():
    embedding = np.array([[[[0, 1]]]], dtype=np.float32)

    segmentation = np.array([[[[-1, 1]]]], dtype=np.int64)

    # number of positive pairs: 0
    # number of negative pairs: 0
    # total number of pairs: 0

    # loss on positive pairs: 0
    # loss on negative pairs: 0
    # total loss: 0

    embedding = torch.from_numpy(embedding).float()
    segmentation = torch.from_numpy(segmentation)

    loss, emst, edges_u, edges_v, distances, *_ = ultrametric_loss(
        embedding,
        segmentation,
        alpha=2,
        balance=True,
        add_coordinates=False,
        constrained_emst=True,
    )

    assert pytest.approx(float(loss)) == 0
    assert pytest.approx(np.sum(distances.numpy())) == 1

    embedding = np.array([[[[0, 1]]]], dtype=np.float32)

    segmentation = np.array([[[[1, -1]]]], dtype=np.int64)

    # number of positive pairs: 0
    # number of negative pairs: 0
    # total number of pairs: 0

    # loss on positive pairs: 0
    # loss on negative pairs: 0
    # total loss: 0

    embedding = torch.from_numpy(embedding).float()
    segmentation = torch.from_numpy(segmentation)

    loss, emst, edges_u, edges_v, distances, *_ = ultrametric_loss(
        embedding,
        segmentation,
        alpha=2,
        balance=True,
        add_coordinates=False,
        constrained_emst=True,
    )

    assert pytest.approx(float(loss)) == 0
    assert pytest.approx(np.sum(distances.numpy())) == 1


def test_ambiguous_ambiguous():
    embedding = np.array([[[[0, 1]]]], dtype=np.float32)

    segmentation = np.array([[[[-1, -1]]]], dtype=np.int64)

    # number of positive pairs: 0
    # number of negative pairs: 0
    # total number of pairs: 0

    # loss on positive pairs: 0
    # loss on negative pairs: 0
    # total loss: 0

    embedding = torch.from_numpy(embedding).float()
    segmentation = torch.from_numpy(segmentation)

    loss, emst, edges_u, edges_v, distances, *_ = ultrametric_loss(
        embedding,
        segmentation,
        alpha=2,
        balance=True,
        add_coordinates=False,
        constrained_emst=True,
    )

    assert pytest.approx(float(loss)) == 0
    assert pytest.approx(np.sum(distances.numpy())) == 1


def test_large_example():
    """
    nodes:              labels:
    [[a, b, c],         [[1, 0, 1],
     [d, e, f],          [2, 2, -1],
     [g, h, i],          [3, 3, 3],
     [j, k, l]]          [0, 0, 0]]
    mst edges (unconstrained), dist, ratio_pos, ratio_neg
    de,                        0     0          0
    ef,                        0     1          0
    jk,                        0     0          0
    ab,                        0.5   0          1
    bc,                        0.5   1          1
    gh,                        1     0          0
    hi,                        1     1          0
    kl,                        1     2          0
    dj,                        1.5   0          9
    fj,                        2     0          13
    gl,                        2     0          24
    mst edges (constrained),   dist, ratio_pos, ratio_neg
    de,                        0     1          0
    jk,                        0     0          0
    ac,                        1     1          0
    gh,                        1     1          0
    hi,                        1     2          0
    kl,                        1     0          0
    bk,                        4     0          0
    ef,                        0     0          0
    ab,                        0.5   0          8
    dj,                        1.5   0          16
    gl,                        2     0          24
    """

    num_pos = 5
    num_neg = 48
    num_edges = num_pos + num_neg

    embedding = np.array(
        [[[[0.5, 1, 1.5], [3.5, 3.5, 3.5], [8, 9, 10], [5, 5, 6]]]], dtype=np.float32
    )

    segmentation = np.array(
        [[[[1, 0, 1], [2, 2, -1], [3, 3, 3], [0, 0, 0]]]], dtype=np.int64
    )

    embedding = torch.from_numpy(embedding).float()
    segmentation = torch.from_numpy(segmentation)

    loss, emst, edges_u, edges_v, distances, *_ = ultrametric_loss(
        embedding,
        segmentation,
        constrained_emst=False,
        balance=False,
        alpha=2,
        add_coordinates=False,
    )

    # numerator = dist**2 * ratio_pos + (alpha-dist)**2 * ratio_neg
    assert pytest.approx(float(loss)) == (3.25 + 6.75) / num_edges
    assert pytest.approx(np.sum(distances.numpy())) == 9.5

    loss, emst, edges_u, edges_v, distances, *_ = ultrametric_loss(
        embedding,
        segmentation,
        constrained_emst=True,
        balance=False,
        alpha=2,
        add_coordinates=False,
    )

    assert pytest.approx(float(loss)) == (4 + 22) / num_edges
    assert pytest.approx(np.sum(distances.numpy())) == 12

    loss, emst, edges_u, edges_v, distances, *_ = ultrametric_loss(
        embedding,
        segmentation,
        constrained_emst=False,
        balance=True,
        alpha=2,
        add_coordinates=False,
    )

    assert pytest.approx(float(loss)) == (3.25 / num_pos + 6.75 / num_neg)
    assert pytest.approx(np.sum(distances.numpy())) == 9.5

    loss, emst, edges_u, edges_v, distances, *_ = ultrametric_loss(
        embedding,
        segmentation,
        constrained_emst=True,
        balance=True,
        alpha=2,
        add_coordinates=False,
    )

    assert pytest.approx(float(loss)) == (4 / num_pos + 22 / num_neg)
    assert pytest.approx(np.sum(distances.numpy())) == 12


def test_quadrupel_loss():

    embedding = np.array([[[[0, 1, 2], [4, 5, 6], [8, 9, 10]]]], dtype=np.float32)

    segmentation = np.array([[[[1, 1, 1], [2, 2, 2], [3, 3, 3]]]], dtype=np.int64)

    # number of positive pairs: 3*3 = 9
    # number of negative pairs: 3*3*3 = 27
    # number of quadrupels: 9*27 = 243

    # loss per quadrupel: max(0, d(p) - d(n) + alpha)^2 = (1 - 2 + 3)^2 = 4

    embedding = torch.from_numpy(embedding).float()
    segmentation = torch.from_numpy(segmentation)

    loss, emst, edges_u, edges_v, distances = ultrametric_loss(
        embedding, segmentation, alpha=3, add_coordinates=False, quadrupel_loss=True,
    )

    assert pytest.approx(float(loss)) == 4.0
    assert pytest.approx(np.sum(distances.numpy())) == 10


def test_add_coordinates():

    embedding = np.array([[[[0, 1, 2], [3, 4, 5], [6, 7, 8]]]], dtype=np.float32)

    segmentation = np.array([[[[1, 1, 1], [2, 2, 2], [3, 3, 3]]]], dtype=np.int64)

    # number of positive pairs: 3*3 = 9
    # number of negative pairs: 3*3*3 = 27
    # total number of pairs: 9*8/2 = 36

    # loss on positive pairs: 9*2 = 18
    # loss on negative pairs: 27*0 = 27
    # total loss = 18
    # total loss per edge = 1

    embedding = torch.from_numpy(embedding).float()
    segmentation = torch.from_numpy(segmentation)

    loss, emst, edges_u, edges_v, distances, *_ = ultrametric_loss(
        embedding, segmentation, alpha=2, add_coordinates=True, balance=False,
    )

    assert pytest.approx(float(loss)) == 18 / 36
    assert (
        pytest.approx(np.sum(distances.numpy()))
        == 6 * (1 ** 2 + 1 ** 2 + 0 ** 2) ** 0.5 + 2 * (2 ** 2 + 1 ** 2 + 1 ** 2) ** 0.5
    )

    loss, emst, edges_u, edges_v, distances, *_ = ultrametric_loss(
        embedding, segmentation, alpha=2, add_coordinates=False,
    )

    assert pytest.approx(float(loss)) == 2.0
    assert pytest.approx(np.sum(distances.numpy())) == 8


@pytest.mark.slow
def test_gradients():
    """
    Naieve test that trains a simple network on a simple
    example and shows that the loss decreases.
    Better test would be to calculate the actual expected
    gradients resulting from a specific loss, and show
    that the back propogation is working as expected.
    """
    n = 50

    embedder = torch.nn.Sequential(
        torch.nn.Conv2d(2, 3, [3, 3], padding=1),
        torch.nn.ReLU(),
        torch.nn.Conv2d(3, 1, [3, 3], padding=1),
        torch.nn.Tanh(),
    )

    raw = torch.Tensor(
        [
            [
                [
                    [0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 2, 0, 0, 0, 0, 2, 0],
                    [0, 1, 0, 0, 0, 0, 1, 0],
                    [0, 1, 0, 0, 0, 0, 1, 0],
                    [0, 1, 0, 0, 0, 0, 1, 0],
                    [0, 1, 0, 0, 0, 0, 1, 0],
                    [0, 2, 0, 0, 0, 0, 2, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0],
                ],
                [
                    [0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 2, 0, 0, 0, 0, 2, 0],
                    [0, 1, 0, 0, 0, 0, 1, 0],
                    [0, 1, 0, 0, 0, 0, 1, 0],
                    [0, 1, 0, 0, 0, 0, 1, 0],
                    [0, 1, 0, 0, 0, 0, 1, 0],
                    [0, 2, 0, 0, 0, 0, 2, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0],
                ],
            ]
        ]
    )
    mask = torch.Tensor(
        [
            [
                [
                    [1, 1, 1, 1, 1, 1, 1, 1],
                    [1, 1, 1, 1, 1, 1, 1, 1],
                    [1, 1, 1, 1, 1, 1, 1, 1],
                    [1, 1, 1, 1, 1, 1, 1, 1],
                    [1, 1, 1, 1, 1, 1, 1, 1],
                    [1, 1, 1, 1, 1, 1, 1, 1],
                    [1, 1, 1, 1, 1, 1, 1, 1],
                    [1, 1, 1, 1, 1, 1, 1, 1],
                ]
            ]
        ]
    ).bool()
    gt_labels = torch.Tensor(
        [
            [
                [
                    [0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 3, 0, 0, 0, 0, 4, 0],
                    [0, 1, 0, 0, 0, 0, 2, 0],
                    [0, 1, 0, 0, 0, 0, 2, 0],
                    [0, 1, 0, 0, 0, 0, 2, 0],
                    [0, 1, 0, 0, 0, 0, 2, 0],
                    [0, 5, 0, 0, 0, 0, 6, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0],
                ]
            ]
        ]
    ).to(torch.int64)

    embeddings = embedder(raw)
    optimizer = torch.optim.Adam(embedder.parameters())
    assert embeddings.shape == (1, 1, 8, 8)

    last_loss = float("inf")
    embedding_vol = np.zeros([n, 8, 8])
    for i in range(n):
        optimizer.zero_grad()
        embeddings = embedder(raw)
        embedding_vol[i, :, :] = embeddings.detach().numpy()[0, 0, :, :]
        loss, *_ = ultrametric_loss(
            embeddings,
            gt_labels,
            mask,
            alpha=0.5,
            coordinate_scale=0.2,
            constrained_emst=False,
        )
        assert float(loss) < float(last_loss)
        assert raw.sum() == 32
        last_loss = loss
        loss.backward()
        optimizer.step()
    np.save("embeddings.npy", embedding_vol)

